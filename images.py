import pygame


def image_loader(image):
    return pygame.image.load(image)


coffee = image_loader("bubbles/coffee.png")
cooking = image_loader("bubbles/cooking.png")
deposit = image_loader("bubbles/Depositing.png")
drink = image_loader("bubbles/Drinking.png")
iron = image_loader("bubbles/ironing.png")
jail = image_loader("bubbles/Jailing.png")
mine = image_loader("bubbles/mining.png")
sleep = image_loader("bubbles/Sleeping.png")

miner_front = image_loader("miner/miner.png")
miner_back = image_loader("miner/minerback.png")
miner_left = image_loader("miner/minerfaceleft.png")
miner_right = image_loader("miner/minerfaceright.png")
