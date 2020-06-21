import irv

# This is just a place to test stuff

irv.Poll()\
    .name("My Poll")\
    .description("This is a poll.")\
    .option("Vanilla")\
    .option("Chocolate")\
    .option("Banana")\
    .create()

print(irv.get_poll("My Poll"))

