library(shiny)
library(magick)

# Rendre les boutons actifs coté client (dans ui)
ui <- fluidPage(
  titlePanel("Dynamic Sign Numeric Vandalizing"),
  sidebarLayout(
    sidebarPanel(
      actionButton("add_sticker", "Add Sticker"),
      selectInput("sticker_choice", "Choose Sticker", choices = NULL),
      sliderInput("x_pos", "X Position", min = 0, max = 1, value = 0.5),
      sliderInput("y_pos", "Y Position", min = 0, max = 1, value = 0.5),
      sliderInput("size", "Size", min = 50, max = 200, value = 100),
      sliderInput("brightness", "Brightness", min = 0, max = 200, value = 100),
      sliderInput("saturation", "Saturation", min = 0, max = 200, value = 100),
      sliderInput("contrast", "Contrast", min = 0, max = 200, value = 100),
      downloadButton("download_image", "Download")
    ),
    mainPanel(
      # Emplacement pour afficher l'image modifiée
      imageOutput("modified_sign_ui")
    )
  )
)

server <- function(input, output, session) {
  # Chemin vers l'image originale et le sticker
  original_path <- "www/Signs/panneau_stop_fr.jpg"
  aim_path <- "www/Aim.png"
  
  # Image originale chargée une seule fois
  original_image <- magick::image_read(original_path)
  aim_image <- magick::image_read(aim_path) %>% 
    magick::image_resize("120x120")
  
  # Utilisez reactiveValues pour conserver l'état de l'image avec les autocollants
  values <- reactiveValues(image = original_image)
  
  stickers <- list.files("www/Stickers", full.names = TRUE)
  sticker_names <- basename(stickers)
  updateSelectInput(session, "sticker_choice", choices = sticker_names, selected = "oops.png")
  
  # Obtenez les dimensions de l'image pour les curseurs
  image_info <- image_info(original_image)
  image_width <- image_info$width
  image_height <- image_info$height
  
  # Image modifiable
  reactive_image <- reactiveVal(original_image)
  
  observe({
    updateSliderInput(session, "x_pos", min = 0, max = image_width, value = image_width / 2)
    updateSliderInput(session, "y_pos", min = 0, max = image_height, value = image_height / 2)
  })
  
  observe({
    x <- as.numeric(input$x_pos)
    y <- as.numeric(input$y_pos)
    brightness_val <- as.numeric(input$brightness)
    saturation_val <- as.numeric(input$saturation)
    contrast_val <- as.numeric(input$contrast)
    
    contrast_scale <- (contrast_val - 100) / 50  # Normaliser autour de 0; ajustez le diviseur pour l'échelle
    
    adjusted_image <- values$image %>%
      magick::image_modulate(brightness = brightness_val, saturation = saturation_val, hue = 100)
    
    if(contrast_scale > 0) {
      # Augmenter le contraste
      adjusted_image <- adjusted_image %>%
        magick::image_contrast(sharpen = TRUE) %>%
        magick::image_contrast(sharpen = TRUE)  # Répétez pour un effet plus fort si nécessaire
    } else if (contrast_scale < 0) {
      # Diminuer le contraste en appliquant un flou
      # L'intensité du flou est ajustée selon la valeur de contrast_scale
      blur_radius <- abs(contrast_scale) * 2  # Ajustez cette formule selon les besoins
      blur_sigma <- abs(contrast_scale)
      adjusted_image <- adjusted_image %>%
        magick::image_blur(radius = blur_radius, sigma = blur_sigma)
    }
    
    # Préparer l'image temporaire avec la cible pour affichage en utilisant l'image ajustée
    temp_image_with_aim <- image_composite(adjusted_image, aim_image, offset = paste0("+", x, "+", y))
    
    # Mise à jour de l'image pour le rendu
    output$modified_sign_ui <- renderImage({
      tempFile <- tempfile(fileext = '.png')
      magick::image_write(temp_image_with_aim, path = tempFile, format = "png")
      
      list(src = tempFile, contentType = 'image/png', width = "100%", alt = "Modified Image")
    }, deleteFile = TRUE)
  })
  
  
  observeEvent(input$add_sticker, {
    sticker_path <- paste0("www/Stickers/", input$sticker_choice)
    size_str <- paste0(input$size, "x", input$size)
    sticker_image <- magick::image_read(sticker_path) %>%
      magick::image_resize(size_str)
    
    x <- as.numeric(input$x_pos)
    y <- as.numeric(input$y_pos)
    
    modified <- image_composite(values$image, sticker_image, offset = paste0("+", x, "+", y))
    values$image <- modified
  })
  
  output$download_image <- downloadHandler(
    filename = function() {
      paste("vandalised_sign_", Sys.Date(), ".png", sep = "")
    },
    content = function(file) {
      x <- as.numeric(input$x_pos)
      y <- as.numeric(input$y_pos)
      brightness_val <- as.numeric(input$brightness)
      saturation_val <- as.numeric(input$saturation)
      contrast_val <- as.numeric(input$contrast)

      contrast_scale <- (contrast_val - 100) / 50  # Normalise around 0; adjust the divisor for scaling

      adjusted_image <- values$image %>%
        magick::image_modulate(brightness = brightness_val, saturation = saturation_val, hue = 100)

      if (contrast_scale > 0) {
        # Increase contrast
        adjusted_image <- adjusted_image %>%
          magick::image_contrast(sharpen = TRUE) %>%
          magick::image_contrast(sharpen = TRUE)  # Repeat for stronger effect if needed
      } else if (contrast_scale < 0) {
        # Decrease contrast by applying blur
        # Blur intensity is adjusted based on the value of contrast_scale
        blur_radius <- abs(contrast_scale) * 2  # Adjust this formula as needed
        blur_sigma <- abs(contrast_scale)
        adjusted_image <- adjusted_image %>%
          magick::image_blur(radius = blur_radius, sigma = blur_sigma)
      }

      # Write the adjusted image to the file
      magick::image_write(adjusted_image, path = file, format = "png")
    }
  )
}

shinyApp(ui = ui, server = server)