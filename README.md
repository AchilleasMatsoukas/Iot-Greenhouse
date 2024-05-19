# Iot-Greenhouse
GreenHouse IOT – Achilleas Matsoukas

  GreenHouse was created using the parameters and the idea of a real GreenHouse and tries to embed all the functions and decisions of a real farmer using a Long-short time memory prediction model based of real time data streams generated by sensors in the Greenhouse.
  
  The hardware that was used is a raspberry pi , a relay module, two dht11 Temperature and Humidity sensors , a 12v DC brushless Fan for cooling, a 5v motor for the side opening, and a 12volt Pump for the watering of the plants.
  
  To create the rule base system, a set of facts was gathered that stated all the possible conditions a cabbage can grow; this included perfect, worst and good values for air-soil temperature and humidity. Using those values, five base rules were created that controlled the system according to what is best for the time. After having all those rules ready, a Long-short time memory prediction model was trained using datasets from the sensors. It was implemented so it can predict near future changes in the Temperatures or Humidity and based on the result it produce a rule is activated doing exactly what a farmer would do. For instance opening the fan or the side door to cool down the insides.
  
  An automated watering system was also implemented, which has a dataset with fixed values for each plant we currently have, the dataset includes the way we must water our plant according to what season we currently on, how much water does it need daily , also how many times a day.
