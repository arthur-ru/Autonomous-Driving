library(shiny)
library(magick)

ui <- fluidPage(
  titlePanel("Dynamic Sign Numeric Vandalizing"),
  sidebarLayout(
    sidebarPanel(
      actionButton("add_sticker", "Add Sticker"),
      sliderInput("x_pos", "X Position", min = 0, max = 1000, value = 500),
      sliderInput("y_pos", "Y Position", min = 0, max = 1000, value = 250),
      sliderInput("size", "Size", min = 50, max = 200, value = 100),
      downloadButton("download_image", "Download")
    ),
    mainPanel(
      # Utilisez le chemin relatif à partir du dossier www
      tags$img(src = "Signs/panneau_stop_fr.jpg", id = "sign_image", style = "width:500px; height:500px;")
    )
  )
)


server <- function(input, output, session) {
  # Chemin vers l'image originale et le sticker
  original_path <- "Signs/panneau_stop_fr.jpg"
  sticker_path <- "Stickers/oops.png" 
  
  # Image originale chargée une seule fois
  original_image <- magick::image_read(original_path)
  
  # Image modifiable
  reactive_image <- reactiveVal(original_image)
  
  observeEvent(input$add_sticker, {
    # Lecture de l'image actuelle et du sticker
    image <- reactive_image()
    sticker <- magick::image_read(sticker_path) %>% 
      magick::image_resize(paste0(input$size, "x", input$size))
    
    # Calcul des coordonnées pour placer le sticker
    x <- input$x_pos
    y <- input$y_pos
    
    # Ajouter le sticker à l'image
    modified <- image_composite(image, sticker, offset = paste0("+", x, "+", y))
    reactive_image(modified)
  })
  
  output$modified_sign <- renderUI({
    # Générer un nom de fichier temporaire pour l'image modifiée
    tempFile <- tempfile(fileext = '.png')
    # Sauvegarder l'image modifiée
    magick::image_write(reactive_image(), path = tempFile, format = "png")
    # Afficher l'image modifiée
    tags$img(src = tempFile, style="width:500px;height:500px;")
  })
  
  output$download_image <- downloadHandler(
    filename = function() {
      paste("vandalised_sign_", Sys.Date(), ".png", sep = "")
    },
    content = function(file) {
      magick::image_write(reactive_image(), path = file, format = "png")
    }
  )
}

shinyApp(ui = ui, server = server)
