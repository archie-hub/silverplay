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


# How to use the helm chart

    x@cabin:~/silverplay$ helm install golddemo  ./goldandsilverstackerhelmchart/ --set-string holdings.silver=888
    NAME: golddemo
    LAST DEPLOYED: Thu Nov 20 17:36:10 2025
    NAMESPACE: kathy
    STATUS: deployed
    REVISION: 1
    TEST SUITE: None
    x@cabin:~/silverplay$ helm upgrade golddemo  ./goldandsilverstackerhelmchart/ --set-string holdings.gold=12
    Release "golddemo" has been upgraded. Happy Helming!
    NAME: golddemo
    LAST DEPLOYED: Thu Nov 20 17:36:40 2025
    NAMESPACE: kathy
    STATUS: deployed
    REVISION: 2
    TEST SUITE: None
    x@cabin:~/silverplay$
