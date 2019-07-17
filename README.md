## Template-game

This is just an outline that I'll use for bigger projects. I try to continously improve it.


# Structure

- **run.py**: run this file to play
- **modules**: custom python modules
  - **game.py**: contains the game controller object that initializes pygame and manages the game states
  - **settings.py**: global game settings that apply to the start of the game
  - **sprites.py**: contains all children of pygame.sprite.Sprite used in the game
  - **states.py**: contains all children of the State class
  - **tilemaps.py**: wrapper for pytmx that creates background images and instantiates sprites from tile data 
- **assets**: graphics and sounds
  - **graphics**: all png files
     - **sprites**:  all sprite images and image strips
     - **tilesets**: all image files used by Tiled
  - **sounds**: all mp3 files
- **data**: all text data (.txt, .json, .xml, .dat ect.)
  - **saves**: ingame save files
  - **tilemaps**: .tsx and .tmx files
