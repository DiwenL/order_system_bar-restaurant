# Order System for bar&restaurant
author: Diwen
date: 2021-07-04
lidiwengz@gmail.com

## Overview
An order system for bar&restaurant. Include touch screen base UI to order food/drinks
Print the receipt.
Summary daily sales.

## Requirement
OS: Windows
Printer: Receipt Printer MJ-5890K, paper width 58mm, USB connect

## Input Files
### menu
food & drink menu for UI setup
located in ./input/menu.txt

max 4 level of selection menu

example format：
__food menu__
__---Soup__
__------Wonton Soup__
__---Fried Rice__
__------Chicken Fried Rice!__
__------Beef Fried Rice!__
__------Pork Fried Rice!__
__---------Extra Egg#__

"---" represent 1 menu level 
"!" represent the order that finally add to receipt
"#" represent the comment



### price
price menu for order setup
located in ./input/price.txt

format:
__[class]name[price]__

example format:
__[food]Chicken Fried Rice[8.5]__
__[beer]Kokanee[6]__

## files
##### seceipt.py
##### order.py
##### main.py
##### ui1920x1080.py
##### summary.py
##### ui1920x1080.ui
##### DBConnector.py