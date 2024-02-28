# SPACE DUEL
#### Video Demo:  <URL HERE>
#### Description:

I wanted to make a game similar to space invaders but player versus player using pygame module in python. I took some inspiration from a youtube pygame tutorial link here(https://www.youtube.com/watch?v=jO6qQDNa2UY&t=3403s&ab_channel=TechWithTim) I referred to the video for the idea and to learn the syntax and tried to code it myself and I added some extra features. Space duel is a game where two ships are controlled by two different players on the same keyboard.
They are seperated by a black border in the middle and can only move around in their zone. Each player has a set amount of lives and ammo(to prevent spamming) that can be changed to the programmer's liking. My code has six total different functions and I will explain them to the best of my ability below. 

The first function is display(), this function is called to fill the screen with the background image and the ship images and 
other things that needs to be displayed like health, ammo etc, using the  .blit() function it projects whatever i need onto the screen, and the function has to end with a .update() to display any changes 
made each time the function is called. 

The next two functions are movement_red and movement_yellow which handles the movements of the spaceships respectively. I used pygame rects to resemble the spaceships. Using the pressed_keys in built function in 
pygame, it can help me detect what button is currently being pressed and using if statements I can output the event according to whichever button is pressed. The math for the d key of the yellow 
ship and the math for the left and right key for the red ship was abit tricky to program I ran into some issues where it would not move or it just would go out of the screen or past the border.

The fourth function is bullet_interaction() which handles what happens if a bullet hits a player and subsequently deducting ammo. I decided to use pygame rects to resemble the bullet and an array to store 
the ammo count. I declared the ammo count array in the main() function and check if the fire key is being pressed down and add a bullet to the array, then in the bullet_interaction() function I used for loops to 
shoot the bullets and used an if collide.rect() function to check if any of the bullets collides with any of the spaceship rects which then queues a 'hit' event into the event queue in the main function, and also 
an else function to check if the bullets go outside of the screen and just removes it.

I also added a powerup feature to the game where a powerup will randomly spawn by constantly generating a number from 1-500 in the main while loop and another random number generator from 1-500 in the pow() function
that is also constantly being called in the main loop. Once both numbers matches each other the variable spawn will let the code know that a powerup should be spawned and using the get_coord() function I return a random x,y coordinate for the powerup to spawn at. There is also an if,else statement towards the end of the while loop to check if a power up has already been spawned so as to tell the code to not spawn any more until the current one gets picked up. Once the random number matches, the code will queue an event called 'Power' in to the event queue, the 'Power' event has a try/except block that essentially  checks if any of the spaceship rects has collided with the powerup rect. If it does collide, it will increase the corresponding spaceship's ammo count and bullet speed, essentially allowing the user to spam bullets. Using an if, else statement and timer variable increment, it essentially times out the power after approximately 10-20 seconds. 

In order to check whoever wins, an if/else statement is constantly checking the spaceship's health each while loop and whenever one reaches 0 it outputs the winner on the screen and breaks out of the loop,and the code restarts after a short period of time. 




