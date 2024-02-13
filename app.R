library(shiny)

# Define UI
ui <- fluidPage(
  headerPanel("Vandalize Signs"),
  sidebarLayout(
    sidebarPanel(
      # Éléments de contrôle, par exemple :
      # actionButton("btn", "Click Me")
    ),
    mainPanel(
      tabsetPanel(type="tab",
                  tabPanel("Sign", img(src="panneau_stop_fr.png", height = "400px"))
      )
    )
  )
)

# Define server logic
server <- function(input, output) {
}

# Run
shinyApp(ui = ui, server = server)