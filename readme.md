# What does this dashboard do

Every minute we go out to

    https://data-asg.goldprice.org/dbXRates/USD

to fetch the current gold and silver prices.

We can set the environmental variables:

* goldholdings
* silverholdings
* myholdingsstring

to determine the value of our holdings.

We can also use the sliders to calculate the value of our holdings if the price of gold or silver changes.


<img src="./images/screenshot.png" alt="dsfsdf" width="75%">

# How to use with docker/podman 
    podman run -d --name silverdaemon -p  5001:5001 albionandrew/goldsilverholdings:v39

or

    podman run  -d --name silverdaemonv3 --env goldholdings=10 --env silverholdings=100 \
    --env myholdingsstring="The chutlers holdings" -p  5002:5001 \
    albionandrew/goldsilverholdings:v39
