import pygame as pg
import random, sys
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QDialog, QRadioButton, QButtonGroup, QLabel, QWidget, QMainWindow, QGridLayout, QLineEdit, QSpacerItem, QPushButton, QVBoxLayout, QColorDialog, QTabWidget, QSizePolicy
from PyQt6.QtGui import QColor
import math
import json


#Child Window
class settings_tab(QWidget):
    

    def __init__(self, parent, colorOfBall, colorOfPaddle, speedOfBall, speedOfOpponent, modeForGame):
        super(QWidget, self).__init__(parent)
        
        self.setStyleSheet("background-color: black;")
        self.setWindowTitle("Settings")

        self.settingsLayout = QVBoxLayout()
        self.pongGUI = parent
        
        #Back button
        #region
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet("border: 2px solid white; background-color: black;")
        self.settingsLayout.addWidget(self.backButton)
        self.backButton.clicked.connect(self.back_button)
        #endregion

        #Initialize content for tabs
        self.color_settings()
        self.ball_difficulty_settings()
        self.cpu_difficulty_settings()
        self.game_mode_settings()

        # create a tab widget
        self.tab = QTabWidget()

        #Players Settings

        self.bColor = colorOfBall
        self.pColor = colorOfPaddle
        self.ballSpeed = speedOfBall
        self.cpuSpeed = speedOfOpponent
        self.gameMode = modeForGame

        print("saved ball", self.bColor.name())
        print("Ball Speed on open", self.ballSpeed)
        print("CPU Speed on open", self.cpuSpeed)
        print("Mode on open: ", self.gameMode)

        #Set up tabs

        #Color Tabs 
        #region
        self.colorsTab = QWidget()
        self.colorsTab.layout = QVBoxLayout()

        self.ballColorLayout = QHBoxLayout() 
        self.ballColorLayout.addWidget(self.ballColorLabel)
        self.ballColorLayout.addWidget(self.ballDisplay)
        
        self.paddleColorLayout = QHBoxLayout()
        self.paddleColorLayout.addWidget(self.paddleColorLabel)
        self.paddleColorLayout.addWidget(self.paddleDisplay)
        
        
        self.colorsTab.layout.addWidget(self.backButton)
        self.backButton.clicked.connect(self.back_button)
        self.colorsTab.layout.addLayout(self.ballColorLayout)
        self.colorsTab.layout.addLayout(self.paddleColorLayout)
        
        self.colorsTab.setLayout(self.colorsTab.layout)
        #endregion

        #Difficulty Tab
        #region
        self.difficultyTab = QWidget()
        self.difficultyTab.layout = QVBoxLayout()
        
        self.ballSpeedLayout = QHBoxLayout()
        self.ballSpeedLayout.addWidget(self.verySlow)
        self.ballSpeedLayout.addWidget(self.slow)
        self.ballSpeedLayout.addWidget(self.medium)
        self.ballSpeedLayout.addWidget(self.fast)
        self.ballSpeedLayout.addWidget(self.veryFast)

        self.cpuSpeedLayout = QHBoxLayout()
        self.cpuSpeedLayout.addWidget(self.cpuVeryEasy)
        self.cpuSpeedLayout.addWidget(self.cpuEasy)
        self.cpuSpeedLayout.addWidget(self.cpuMedium)
        self.cpuSpeedLayout.addWidget(self.cpuHard)
        self.cpuSpeedLayout.addWidget(self.cpuVeryHard)

        self.difficultyTab.layout.addWidget(self.ballSpeedLabel)
        self.difficultyTab.layout.addLayout(self.ballSpeedLayout)
        self.difficultyTab.layout.addWidget(self.cpuSpeedLabel)
        self.difficultyTab.layout.addLayout(self.cpuSpeedLayout)
        
        self.difficultyTab.setLayout(self.difficultyTab.layout)
        #endregion

        #game mode tab
        #region
        self.gameModeTab = QWidget()
        self.gameModeTab.layout = QVBoxLayout()

        self.gameModeTab.layout.addWidget(self.originalMode)
        self.gameModeTab.layout.addWidget(self.originalDescription)
        self.gameModeTab.layout.addWidget(self.infiniteMode)
        self.gameModeTab.layout.addWidget(self.infiniteDescription)
        


        self.gameModeTab.setLayout(self.gameModeTab.layout)
        #endregion

        #Add tabs
        #region
        self.tab.addTab(self.colorsTab, "Colours")
        self.tab.addTab(self.difficultyTab, "Difficulty")
        self.tab.addTab(self.gameModeTab, "Game Mode")
        #endregion

        #Styles
        self.tab.setStyleSheet(f"""
            
            QTabWidget::pane {{
                border-top: 0px;
                padding: 2px;
                
                
            }}

            QTabWidget::tab-bar {{
                left: 5px; 
                top: 10px;
                
            }}


            QTabBar::tab {{
                background: #606060;
                border: 2px solid #0020b3;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                min-width: 16ex;
                font: 16px;
                color: #000000;
                padding: 2px;
            }}

            QTabBar::tab:hover {{
                background: #707070;
            }}

            QTabBar::tab:selected {{
                border-color: #0020b3;
                border-bottom-color: #000000;
                background: #000000;
                color: #00208b;
            }}

            QTabBar::tab:!selected {{
                margin-top: 2px; 
            }}
""")
            
        self.settingsLayout.addWidget(self.tab)
        self.setLayout(self.settingsLayout)

        self.show()
    
    def back_button(self):
        
        self.clear_settings_layout(self.settingsLayout)
        self.pongGUI.reset_layout()
             
    def clear_settings_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()        
        else:
            return
        

    # COLORS TAB
    #region
       
    def color_settings(self):
        self.bColor = QColor(255, 255, 255)
        self.ballColorLabel = QLabel("Ball Colour")
        self.ballColorLabel.setStyleSheet("font: white; font-size: 16px; line-height: 18px;")
        
        self.ballDisplay = QPushButton()
        self.ballDisplay.clicked.connect(self.ball_color)
        self.ballDisplay.setFixedSize(300, 50)
        self.ballDisplay.setStyleSheet(f"background-color: {self.bColor.name()};")

        self.pColor = QColor(255, 255, 255)
        self.paddleColorLabel = QLabel("Paddle Color")
        self.paddleColorLabel.setStyleSheet("font: white; font-size: 16px;")
        self.paddleDisplay = QPushButton()
        self.paddleDisplay.clicked.connect(self.paddle_color)
        self.paddleDisplay.setFixedSize(300, 50)
        self.paddleDisplay.setStyleSheet(f"background-color: {self.pColor.name()};")

    def ball_color(self):
        self.bColor = QColorDialog.getColor(self.bColor)
        
        if self.bColor.isValid():
            self.ballDisplay.setStyleSheet(f"background-color: {self.bColor.name()}")
            
            self.pongGUI.colorOfBall = self.bColor
        
    def paddle_color(self):
        self.pColor = QColorDialog.getColor()
        if self.pColor.isValid():
            self.paddleDisplay.setStyleSheet(f"background-color: {self.pColor.name()}")
    
            self.pongGUI.colorOfPaddle = self.pColor
        
    def update_color_display(self):
        self.ballDisplay.setStyleSheet(f"background-color: {self.bColor.name()}")

        self.paddleDisplay.setStyleSheet(f"background-color: {self.pColor.name()}")
    #endregion
    
    # DIFFICULTY TAB
    #region
    def ball_difficulty_settings(self):

        #Ball Speed Settings
        #region
        self.ballSpeedLabel = QLabel("Ball Speed")
        self.ballSpeedLabel.setStyleSheet("color: white; font-size: 16px;")
        self.ballSpeed = 0.6

        self.verySlow = QRadioButton("Very Slow")
        self.slow = QRadioButton("Slow")
        self.medium = QRadioButton("Medium")
        self.fast = QRadioButton("Fast")
        self.veryFast = QRadioButton("Very Fast")

        self.ballSpeedGroup = QButtonGroup()
        self.ballSpeedGroup.addButton(self.verySlow)
        self.ballSpeedGroup.addButton(self.slow)
        self.ballSpeedGroup.addButton(self.medium)
        self.ballSpeedGroup.addButton(self.fast)
        self.ballSpeedGroup.addButton(self.veryFast)
        
        self.verySlow.clicked.connect(self.update_ball_speed)
        self.slow.clicked.connect(self.update_ball_speed)
        self.medium.clicked.connect(self.update_ball_speed)
        self.fast.clicked.connect(self.update_ball_speed)
        self.veryFast.clicked.connect(self.update_ball_speed)

        #endregion

    def cpu_difficulty_settings(self):
        #CPU Settings
        #region
        self.cpuSpeedLabel = QLabel("Opponent Difficulty")
        self.cpuSpeedLabel.setStyleSheet("color: white; font-size: 16px;")
        self.cpuSpeed = 0.6

        self.cpuVeryEasy = QRadioButton("Very Easy")
        self.cpuEasy = QRadioButton("Easy")
        self.cpuMedium = QRadioButton("Medium")
        self.cpuHard = QRadioButton("Hard")
        self.cpuVeryHard = QRadioButton("Very Hard")

        self.cpuSpeedGroup = QButtonGroup()
        self.cpuSpeedGroup.addButton(self.cpuVeryEasy)
        self.cpuSpeedGroup.addButton(self.cpuEasy)
        self.cpuSpeedGroup.addButton(self.cpuMedium)
        self.cpuSpeedGroup.addButton(self.cpuHard)
        self.cpuSpeedGroup.addButton(self.cpuVeryHard)

        self.cpuVeryEasy.clicked.connect(self.update_cpu_difficulty)
        self.cpuEasy.clicked.connect(self.update_cpu_difficulty)
        self.cpuMedium.clicked.connect(self.update_cpu_difficulty)
        self.cpuHard.clicked.connect(self.update_cpu_difficulty)
        self.cpuVeryHard.clicked.connect(self.update_cpu_difficulty)
        #endregion

    def update_ball_speed(self):

        # Changes Ball Speed attribute
        if self.verySlow.isChecked():
            self.ballSpeed = 2
            print("Saved speed", self.ballSpeed)
        elif self.slow.isChecked():
            self.ballSpeed = 3
            print("Saved speed", self.ballSpeed)
        elif self.medium.isChecked():
            self.ballSpeed = 5
            print("Saved speed", self.ballSpeed)
        elif self.fast.isChecked():
            self.ballSpeed = 6.5
            print("Saved speed", self.ballSpeed)
        elif self.veryFast.isChecked():
            self.ballSpeed = 8
            print("Saved speed", self.ballSpeed)

        self.pongGUI.speedOfBall = self.ballSpeed

        # For showing which speed is selected
        if self.ballSpeed == 0.2:
            self.verySlow.setChecked(True)
        elif self.ballSpeed == 0.4:
            self.slow.setChecked(True)
        elif self.ballSpeed == 0.6:
            self.medium.setChecked(True)
        elif self.ballSpeed == 0.8:
            self.fast.setChecked(True)
        elif self.ballSpeed == 1.0:
            self.veryFast.setChecked(True)

    def update_cpu_difficulty(self):
        if self.cpuVeryEasy.isChecked():
            self.cpuSpeed = 2
            print("Saved CPU Speed", self.cpuSpeed)
        elif self.cpuEasy.isChecked():
            self.cpuSpeed = 4
            print("Saved CPU Speed", self.cpuSpeed)
        elif self.cpuMedium.isChecked():
            self.cpuSpeed = 6
            print("Saved CPU Speed", self.cpuSpeed)
        elif self.cpuHard.isChecked():
            self.cpuSpeed = 8
            print("Saved CPU Speed", self.cpuSpeed)
        elif self.cpuVeryHard.isChecked():
            self.cpuSpeed = 10
            print("Saved CPU Speed", self.cpuSpeed)
        
        self.pongGUI.speedOfOpponent = self.cpuSpeed

        if self.cpuSpeed == 0.2:
            self.cpuVeryEasy.setChecked(True)
        elif self.cpuSpeed == 0.4:
            self.cpuEasy.setChecked(True)
        elif self.cpuSpeed == 0.6:
            self.cpuMedium.setChecked(True)
        elif self.cpuSpeed == 0.8:
            self.cpuHard.setChecked(True)
        elif self.cpuSpeed == 1.0:
            self.cpuVeryHard.setChecked(True)
    #endregion

    def game_mode_settings(self):
        self.gameModeLabel = QLabel("Choose Game Mode")
        self.gameModeLabel.setStyleSheet("color: white; font-size: 16px;")
        self.gameMode = 1

        self.originalMode = QRadioButton("Original")
        self.originalDescription = QLabel("Classic Pong versus computer. First to 11 wins.")
        self.originalDescription.setWordWrap(True)
        self.originalDescription.setStyleSheet("color: white; font-size: 14px;")

        self.infiniteMode = QRadioButton("Infinite Pong")
        self.infiniteDescription = QLabel("Single player, ball is hit against the wall, increasing with speed over time. Game ends when you miss the ball")
        self.infiniteDescription.setWordWrap(True)
        self.infiniteDescription.setStyleSheet("color: white; font-size: 14px;")

        self.originalMode.clicked.connect(self.update_game_mode)
        self.infiniteMode.clicked.connect(self.update_game_mode)
    
    def update_game_mode(self):

        if self.originalMode.isChecked():
            self.gameMode = 1
            print("Game Mode: Original")
        elif self.infiniteMode.isChecked():
            self.gameMode = 2
            print("Game Mode: Infinite")

        self.pongGUI.modeForGame = self.gameMode

        if self.gameMode == 1:
            self.originalMode.setChecked(True)
        elif self.gameMode == 2:
            self.infiniteMode.setChecked(True)

class pong_GUI(QMainWindow):

    def __init__(self): 
        super().__init__()
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        self.mainWindow = QVBoxLayout(centralWidget)
        self.setWindowTitle("Pong")
        self.setGeometry(500, 500, 500, 500)
        centralWidget.setStyleSheet("background-color: black;")


        self.colorOfBall = QColor(255, 255, 255)
        self.colorOfPaddle = QColor(255, 255, 255)
        self.speedOfBall = 5
        self.speedOfOpponent = 6
        self.modeForGame = 1
        self.settingsTab = settings_tab(self, self.colorOfBall, self.colorOfPaddle, self.speedOfBall, self.speedOfOpponent, self.modeForGame)
        

        
        self.attributes()
        self.buttons()
        self.layout()

        print(self.modeForGame)
        
    def attributes(self):
        self.buttonSize = (200, 50)
        self.buttonBackColor = 105, 105, 105
        self.buttonBorderColor = 0, 32, 179
        self.buttonHoverBack = 67, 67, 67
        self.buttonHoverBorder = 0, 32, 139

    def buttons(self):

        #Settings Button
        #region
        self.settingsButton = QPushButton("Settings")
        self.settingsButton.setFixedSize(*self.buttonSize)
        self.settingsButton.setStyleSheet(f"QPushButton {{background-color: rgb{self.buttonBackColor}; color: black; font: 18px; border-style: solid; border-width: 4px; border-color: rgb{self.buttonBorderColor};}} QPushButton:hover {{background-color: rgb{self.buttonHoverBack}; border-color: rgb{self.buttonHoverBorder}}}")
        self.settingsButton.clicked.connect(self.open_settings)
        #endregion

        #Start Button
        #region
        self.startButton = QPushButton("Start Game")
        self.startButton.setFixedSize(*self.buttonSize)
        self.startButton.setStyleSheet(f"QPushButton {{background-color: rgb{self.buttonBackColor}; color: black; font: 18px; border-style: solid; border-width: 4px; border-color: rgb{self.buttonBorderColor};}} QPushButton:hover {{background-color: rgb{self.buttonHoverBack}; border-color: rgb{self.buttonHoverBorder}}}")
        self.startButton.clicked.connect(self.start_game)
        #endregion

    def open_settings(self):
        self.clearLayout(self.mainWindow)
        settingsTab = settings_tab(self, self.colorOfBall, self.colorOfPaddle, self.speedOfBall, self.speedOfOpponent, self.modeForGame)

        settingsTab.resize(500, 200)

        settingsTab.show()
        
    def start_game(self):
        

        if self.modeForGame == 1:
            self.clearLayout(self.mainWindow)
            self.startOriginalGame = start_pong(self.colorOfBall, self.colorOfPaddle, self.speedOfOpponent, self.speedOfBall)
            self.startOriginalGame.__init__()
            print("Starting Original")
        
        elif self.modeForGame == 2:
            self.clearLayout(self.mainWindow)
            self.startInfiniteGame = infinite_pong(self.colorOfBall, self.colorOfPaddle)
            self.startInfiniteGame.__init__()
            print("Starting Infinite")

    def restart_original(self):
        pass

    def restart_infinite(self):
        self.clearLayout(self.mainWindow)
        self.startInfiniteGame = infinite_pong(self.colorOfBall, self.colorOfPaddle)
        self.startInfiniteGame.__init__()
        print("Starting Infinite")
    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()        
        else:
            return

    def layout(self):
        self.mainWindow.addWidget(self.settingsButton, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        self.mainWindow.addWidget(self.startButton, 0, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def reset_layout(self):
        self.clearLayout(self.mainWindow)
        self.attributes()
        self.buttons()
        self.layout()
        print("Reset_layout")
        print("Game Mode: ", self.modeForGame)
        print("Speed: ", self.speedOfBall)

class start_pong():

    def __init__(self, colorOfBall, colorOfPaddle, speedOfOpponent, speedOfBall):
        pg.init()

        self.gameScreenWidth = 1000
        self.gameScreenHeight = 800
        self.gameScreen = pg.display.set_mode((self.gameScreenWidth, self.gameScreenHeight))
        hidden = pg.HIDDEN

        self.winOverlay = pg.Surface((500, 200))
        self.winOverlay.fill((100, 100, 100))
        self.winOverlayCenter = self.winOverlay.get_rect(center=(500, 400))
        self.winOverlayBorder = 3
        self.winOverlayBorderColor = (255, 0, 0)

        self.playerScore = 00
        self.cpuScore = 00

        self.gameSettings = pong_GUI()
        gamePaused = False

        # Ball Attributes
        #region
        self.colorBall = (colorOfBall.red(), colorOfBall.green(), colorOfBall.blue())
        self.colorPaddle = (colorOfPaddle.red(), colorOfPaddle.green(), colorOfPaddle.blue())
        self.ballWidth = 20
        self.ballHeight = 20
        self.ballXPosition = 140
        self.ballYPosition = 140
        self.ballXVelocity = speedOfBall
        self.ballYVelocity = speedOfBall
        self.ballColor = self.colorBall
        self.ballSpeed = speedOfBall
        #endregion

        #Player Paddle Attributes
        #region
        self.playerPaddleWidth = 15
        self.playerPaddleHeight = 100
        self.playerPaddleXPosition = 35
        self.playerPaddleYPosition = 100
        self.playerPaddleColor = self.colorPaddle
        self.playerPaddleSpeed = 5
        #endregion
        
        #CPU Paddle Attributes
        #region
        self.cpuPaddleWidth = 15
        self.cpuPaddleHeight = 100
        self.cpuPaddleXPosition = ((self.gameScreenWidth - self.cpuPaddleWidth) - 35)   
        self.cpuPaddleYPosition = 100 
        self.cpuPaddleColor = self.colorPaddle
        self.cpuPaddleSpeed = speedOfOpponent
        #endregion
        

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_r and gamePaused:
                        gamePaused = False
                        self.playerScore = 0
                        self.cpuScore = 0
                        self.draw_ball()
                        self.ballXPosition
                        self.ballYPosition
                                
                    
                    elif event.key == pg.K_q and gamePaused:
                        gamePaused = False
                        running = False
                        pg.quit()
                                
                    
                    elif event.key == pg.K_m and gamePaused:
                        self.gameScreen = pg.display.set_mode((self.gameScreenWidth, self.gameScreenHeight), flags=pg.HIDDEN)
                        self.gameSettings.show()
                        
                        
            

            if gamePaused == False:
                self.gameScreen.fill((0, 0, 0))
                self.draw_player_paddle()
                self.draw_cpu_paddle()
                self.draw_lines()
                self.draw_player_scores()
                self.draw_cpu_scores()
                self.draw_ball()
                self.player_win_message()
                self.cpu_win_message()
                self.pause_options()

            

                self.gameScreen.blit(self.drawPlayerScore, (350, 5, 50, 50))
                self.gameScreen.blit(self.drawCPUScore, (550, 5, 50, 50))
                self.ballXPosition += self.ballXVelocity
                self.ballYPosition += self.ballYVelocity
        

                #Ball Screen Collision
                #region

                #Ball Wall Collision
                if self.ballXPosition >= (self.gameScreenWidth + self.ballWidth): 
                    self.reset_ball( self.gameScreenWidth, self.gameScreenHeight)
                    self.playerScore += 1
                        
                        
                    print(self.playerScore)
                    
                elif self.ballXPosition <= 0:
                    self.reset_ball( self.gameScreenWidth, self.gameScreenHeight)
                    self.cpuScore += 1
                        
                    print(self.cpuScore)



                    
                #Ball top/bottom Collision
                if self.ballYPosition <= self.horizontalYPosition + 2:
                    self.ballYVelocity = -self.ballYVelocity
                if self.ballYPosition + self.ballHeight >= self.gameScreenHeight:
                    self.ballYVelocity = -self.ballYVelocity
                    #endregion
                    
                #Handle Player Paddle Movement
                #region
                key = pg.key.get_pressed()
                if key[pg.K_UP]:
                    self.playerPaddleYPosition -= self.playerPaddleSpeed
                    if self.playerPaddleYPosition <= self.horizontalYPosition:
                        self.playerPaddleYPosition = self.horizontalYPosition

                if key[pg.K_DOWN]:   
                    self.playerPaddleYPosition += self.playerPaddleSpeed
                    if self.playerPaddleYPosition + self.playerPaddleHeight >= self.gameScreenHeight:
                        self.playerPaddleYPosition = self.gameScreenHeight - self.playerPaddleHeight
                    
                #endregion
                    

                #Handle Ball/Player Collision
                if self.ball.colliderect(self.playerPaddle):
                    self.player_ball_bounce(self.playerPaddleYPosition, self.playerPaddleHeight)
                        
                #Handle CPU Paddle Movement
                #region
                if self.ballYPosition < self.cpuPaddleYPosition:
                    self.cpuPaddleYPosition -= self.cpuPaddleSpeed
                elif self.ballYPosition > (self.cpuPaddleYPosition + self.cpuPaddleHeight):
                    self.cpuPaddleYPosition += self.cpuPaddleSpeed
                #endregion

                    
                #Handle Ball/CPU Collision
                if self.ball.colliderect(self.cpuPaddle):
                    self.cpu_ball_bounce(self.cpuPaddleYPosition, self.cpuPaddleHeight)
                    
                    
                
                
                #Player Win Event
                if self.playerScore == 3:
                    gamePaused = True
                    

                if self.cpuScore == 1:
                    gamePaused = True
                    

            if gamePaused == True:

                if self.playerScore == 3:
                    pg.draw.rect(self.winOverlay, self.winOverlayBorderColor, self.winOverlay.get_rect(), self.winOverlayBorder)

                    self.gameScreen.blit(self.winOverlay, self.winOverlayCenter.topleft)

                    self.winOverlay.blit(self.drawPlayerWin, (100, 50, 100, 100))
                    self.winOverlay.blit(self.drawPauseOptions, (100, 150, 100, 100))
                            
                if self.cpuScore == 1:
                    pg.draw.rect(self.winOverlay, self.winOverlayBorderColor, self.winOverlay.get_rect(), self.winOverlayBorder)

                    self.gameScreen.blit(self.winOverlay, self.winOverlayCenter.topleft)

                    self.winOverlay.blit(self.drawCPUWin, (100, 50, 100, 100))

                    self.winOverlay.blit(self.drawPauseOptions, (100, 150, 100, 100))


            pg.display.flip()

            pg.time.Clock().tick(60)
        
        
        
        pg.display.quit()
        

    def draw_ball(self):
      
        self.ball = pg.draw.rect(self.gameScreen, self.colorBall, (self.ballXPosition, self.ballYPosition, self.ballWidth, self.ballHeight))
        

        return self.ball

    def draw_player_paddle(self):
        
        self.playerPaddle = pg.draw.rect(self.gameScreen, self.colorPaddle, (self.playerPaddleXPosition, self.playerPaddleYPosition, self.playerPaddleWidth, self.playerPaddleHeight))

        return self.playerPaddle

    def draw_cpu_paddle(self):
        
        self.cpuPaddle = pg.draw.rect(self.gameScreen, self.colorPaddle, (self.cpuPaddleXPosition, self.cpuPaddleYPosition, self.cpuPaddleWidth, self.cpuPaddleHeight))

        return self.cpuPaddle

    def draw_lines(self):
        #Horizontal Top Line
        self.horizontalWidth = self.gameScreenWidth
        self.horizontalHeight = 5
        self.horizontalXPosition = 0
        self.horizontalYPosition = 80
        self.horizontalColor = (255, 255, 255)
        self.horizontalLine = pg.draw.rect(self.gameScreen, self.horizontalColor, (self.horizontalXPosition, self.horizontalYPosition, self.horizontalWidth, self.horizontalHeight))

        # Vertical Center Line
        self.verticalWidth = 5
        self.verticalHeight = self.gameScreenHeight
        self.verticalXPosition = (self.gameScreenWidth / 2) - self.verticalWidth
        self.verticalYPosition = 0
        self.verticalColor = (255, 255, 255)
        self.verticalLine = pg.draw.rect(self.gameScreen, self.verticalColor, (self.verticalXPosition, self.verticalYPosition, self.verticalWidth, self.verticalHeight))

    def draw_player_scores(self):
        
        self.scoreFont = pg.font.SysFont(None, 100)
        

        self.drawPlayerScore = self.scoreFont.render(f"{self.playerScore: 00}", True, (255, 255, 255))

        return self.drawPlayerScore

    def draw_cpu_scores(self):
        
        self.scoreFont = pg.font.SysFont(None, 100)
        

        self.drawCPUScore = self.scoreFont.render(f"{self.cpuScore: 00}", True, (255, 255, 255))

        return self.drawCPUScore

    def player_ball_bounce(self, playerPaddleY, playerPaddleH):
        maxBallBounce = 5 * math.pi/12

        # The difference between the ball and paddle centre

        #Get centre of ball
        ballPlayerIntersectY = self.ballYPosition + self.ballHeight / 2 
        ballPaddleRelativeY = (playerPaddleY + (playerPaddleH / 2)) - ballPlayerIntersectY

        #Scale down the result
        normalizeBallPaddY = ballPaddleRelativeY / (playerPaddleH / 2)

        #Calculate bounce angle
        playerBounceAngle = normalizeBallPaddY * maxBallBounce

        #Calculate ball speed
        ballSpeed = math.sqrt(self.ballXVelocity**2 + self.ballYVelocity**2)

        #Update Velocities
        self.ballXVelocity = abs(ballSpeed) * math.cos(playerBounceAngle)
        self.ballYVelocity = -abs(ballSpeed) * math.sin(playerBounceAngle)

    def cpu_ball_bounce(self, cpuPaddleY, cpuPaddleH):
        maxBallBounceCpu = 5 * math.pi/12

        # The difference between the ball and paddle centre

        #Get centre of ball
        ballCpuIntersectY = self.cpuPaddleYPosition+ self.ballHeight / 2 
        ballCpuPaddleRelativeY = (cpuPaddleY + (cpuPaddleH / 2)) - ballCpuIntersectY

        #Scale down the result
        normalizeBallCpuPaddY = ballCpuPaddleRelativeY / (cpuPaddleH / 2)

        #Calculate bounce angle
        cpuBounceAngle = normalizeBallCpuPaddY * maxBallBounceCpu

        #Calculate ball speed
        ballSpeedCpu = math.sqrt(self.ballXVelocity**2 + self.ballYVelocity**2)

        #Update Velocities
        self.ballXVelocity = -abs(ballSpeedCpu) * math.cos(cpuBounceAngle)
        self.ballYVelocity = abs(ballSpeedCpu) * math.sin(cpuBounceAngle)

    def reset_ball(self, screenWidth, screenHeight):
        
            
            newBallX = round(screenWidth / 2)
            newBallY = round(screenHeight / 2)

            self.ballXPosition = newBallX
            self.ballYPosition = newBallY

            newBallSpeed = random.choice([-self.ballSpeed, self.ballSpeed])

            self.ballXVelocity = newBallSpeed
            self.ballYVelocity = newBallSpeed

    def player_win_message(self):
        self.playerWin = pg.font.SysFont(None, 50)

        self.drawPlayerWin = self.playerWin.render("Player Wins!", True, (0, 0, 0))
        
        return self.drawPlayerWin
    
    def cpu_win_message(self):
        self.cpuWin = pg.font.SysFont(None, 50)
        self.drawCPUWin = self.cpuWin.render("Computer Wins!", True, (0, 0, 0))

        return self.drawCPUWin
    
    def pause_options(self):
        self.pauseFont = pg.font.SysFont(None, 30)

        self.drawPauseOptions = self.pauseFont.render("[Q] Quit | [M] Menu | [R] Restart", True, (0, 0, 0))

        return self.drawPauseOptions

    def pause_game(self):
        global running
        global gamePaused
        gamePaused = True
        self.mainGUI = pong_GUI()
        
        while gamePaused:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        gamePaused = False
                        self.playerScore = 0
                        self.cpuScore = 0
                        self.draw_ball()
                        self.ballXPosition
                        self.ballYPosition
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        gamePaused = False
                        running = False
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_m:
                        gamePaused = False
                        running = False
                        self.mainGUI.show()

class infinite_pong():

    def __init__(self, colorOfBall, colorOfPaddle):
        pg.init()

        self.infiniteScreenWidth = 1000
        self.infiniteScreenHeight = 800
        self.infiniteScreen = pg.display.set_mode((self.infiniteScreenWidth, self.infiniteScreenHeight))
        hidden = pg.HIDDEN

        self.infEndOverlay = pg.Surface((500, 200))
        self.infEndOverlay.fill((100, 100, 100))
        self.infEndOverlayCenter = self.infEndOverlay.get_rect(center=(500, 400))
        self.infEndOverlayBorder = 3
        self.infEndOverlayBorderColor = (255, 0, 0)

        self.infScore = 0
        self.lastTime = 0
        self.infLevel = 1
        self.lastLevelupTime = 0
        self.infClock = pg.time.Clock()

        self.gameSettings = pong_GUI()
        infPaused = False
        infRunning = True


        self.infiniteColorBall = (colorOfBall.red(), colorOfBall.green(), colorOfBall.blue())
        self.infiniteColorPaddle = (colorOfPaddle.red(), colorOfPaddle.green(), colorOfPaddle.blue())
        
        # Ball Attributes
        #region
        self.infBallWidth = 20
        self.infBallHeight = 20
        self.infBallXPosition = 140
        self.infBallYPosition = 140
        self.infBallColor = self.infiniteColorBall
        #pixels per second. Originall 5 px/frame, 60fps (5*60 = 300)
        self.infBallSpeed = 300 
        
        
        self.infBallXVelocity = self.infBallSpeed
        self.infBallYVelocity = self.infBallSpeed
        #endregion

        #Player Paddle Attributes
        #region
        self.infinitePaddleWidth = 15
        self.infinitePaddleHeight = 100
        self.infinitePaddleXPosition = 35
        self.infinitePaddleYPosition = 100
        self.infinitePaddleColor = self.infiniteColorPaddle
        self.infinitePaddleSpeed = 5
        #endregion
        
        while infRunning:
            for event in pg.event.get():
                if event == pg.QUIT:
                    infRunning = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_r and infPaused:
                        self.infScore = 0
                        self.infLevel = 0
                        self.gameSettings.restart_infinite()

                                
                    
                    elif event.key == pg.K_q and infPaused:
                        infPaused = False
                        infRunning = False
                        pg.quit()
                                
                    
                    elif event.key == pg.K_m and infPaused:
                        self.infiniteScreen = pg.display.set_mode((self.infiniteScreenWidth, self.infiniteScreenHeight), flags=pg.HIDDEN)
                        self.gameSettings.show()
                

       
            if infPaused == False:
                self.infiniteScreen.fill((0, 0, 0))
                
                self.infinite_paddle()
                self.infinite_ball()
                self.infinite_score()
                self.infinite_level()
                self.infinite_end_game()
                self.infinite_final_level()
                self.infinite_final_score()
                self.infinite_pause_options()
                self.infinite_show_High_Score()

                self.infiniteScreen.blit(self.inf_drawHighScore, (self.infiniteScreenWidth - (self.highScoreW + 50), 5, 50, 50))

                self.infiniteScreen.blit(self.inf_drawHighLevel, (self.infiniteScreenWidth - (self.highLevelW + 50), 30, 50, 50))

                self.infiniteScreen.blit(self.inf_drawScore, (50, 5, 50, 50))
                self.infiniteScreen.blit(self.inf_drawLevel, (50, 30, 50, 50))
                self.deltaTime = self.infClock.tick(60) / 1000
                self.infBallXPosition += self.infBallXVelocity * self.deltaTime
                self.infBallYPosition += self.infBallYVelocity * self.deltaTime
                


            #Ball Screen Collision Side
                if self.infBallXPosition >= self.infiniteScreenWidth - self.infBallWidth:
                    self.infBallXVelocity = -self.infBallXVelocity

            #Ball top/bottom collision
                if self.infBallYPosition <= 0:
                    self.infBallYVelocity = -self.infBallYVelocity

                if self.infBallYPosition >= self.infiniteScreenHeight - self.infBallHeight:
                    self.infBallYVelocity = -self.infBallYVelocity 

            #Paddle Movement 
                self.inf_mousePosition = pg.mouse.get_pos()
                pg.mouse.set_visible(False)
                self.infinitePaddleYPosition = self.inf_mousePosition[1]
                

            #Ball/Paddle Collision
                if self.infiniteBall.colliderect(self.infinitePaddle):
                    self.infinite_bounce(self.infinitePaddleYPosition, self.infinitePaddleHeight)

            #Scoring
                self.infiniteTime = pg.time.get_ticks() // 1000
                if self.infiniteTime != self.lastTime:
                    self.infScore = self.infiniteTime
                

            #Speed up ball over time
                if self.infiniteTime % 10 == 0 and self.infiniteTime != self.lastLevelupTime:
                    # originally increased by 5px/frame @ 60fps (300/second)
                    self.infBallSpeed += 300
                    self.infLevel += 1
                    print("Ball Speed", self.infBallSpeed)
                    self.lastLevelupTime = self.infiniteTime

            #End Game
                if self.infBallXPosition <= 0:
                    infPaused = True
                    self.infinite_save(self.infScore, self.infLevel)
            
            if infPaused == True:
                pg.draw.rect(self.infEndOverlay, self.infEndOverlayBorderColor, self.infEndOverlay.get_rect(), self.infEndOverlayBorder)

                self.infiniteScreen.blit(self.infEndOverlay, self.infEndOverlayCenter.topleft)

                self.infEndOverlay.blit(self.inf_drawEnd, (250 - self.drawEndW, 30, 100, 100))

                self.infEndOverlay.blit(self.inf_drawFinalScore, (50, 90, 100, 100))
                
                self.infEndOverlay.blit(self.inf_drawFinalLevel, (450 - self.finalLevelW, 90, 100, 100))

                self.infEndOverlay.blit(self.inf_PauseOptions, (100, 170 - self.pauseOptionsH, 100, 100))


            pg.display.flip()

            pg.time.Clock().tick(120)
        
        
        
        pg.display.quit()
              
    def infinite_save(self, score, level, filename='infinite-scores.json'):
        data = {"score": score, "level": level}
        try:
            with open(filename, 'r') as file:
                scores = json.load(file)
        except FileNotFoundError:
            scores = []
        
        scores.append(data)
        
        with open(filename, 'w') as file:
            json.dump(scores, file)

    def infinite_load(self, filename='infinite-scores.json'):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                if not data:
                    return None, None
                maxScore = max(item['score'] for item in data)
                maxLevel = max(item['level'] for item in data)
                return maxScore, maxLevel
        except FileNotFoundError:
            return None, None
            
    def infinite_show_High_Score(self):
        self.inf_maxScore, self.inf_maxLevel = self.infinite_load()

        self.inf_highScoreFont = pg.font.SysFont("Arial", 18)
        self.inf_highLevelFont = pg.font.SysFont("Arial", 18)

        self.inf_drawHighScore = self.inf_highScoreFont.render(f"High Score: {self.inf_maxScore}", True, (255, 255, 255))
        self.inf_drawHighLevel = self.inf_highLevelFont.render(f"High Level: {self.inf_maxLevel}", True, (255, 255, 255))

        self.highScoreW = self.inf_drawHighScore.get_width()
        self.highLevelW = self.inf_drawHighLevel.get_width()

        return self.inf_drawHighScore, self.inf_drawHighLevel

    def infinite_ball(self):
        self.infiniteBall = pg.draw.rect(self.infiniteScreen, self.infiniteColorBall, (self.infBallXPosition, self.infBallYPosition, self.infBallWidth, self.infBallHeight))

        return self.infiniteBall

    def infinite_paddle(self):
        self.infinitePaddle = pg.draw.rect(self.infiniteScreen, self.infiniteColorPaddle, (self.infinitePaddleXPosition, self.infinitePaddleYPosition, self.infinitePaddleWidth, self.infinitePaddleHeight))

        return self.infinitePaddle

    def infinite_bounce(self, paddleY, paddleH):
        maxBounce = 5 * math.pi/12

        # The difference between the ball and paddle centre

        #Get centre of ball
        ballPadIntersectY = self.infBallYPosition + self.infBallHeight / 2 
        ballPadRelativeY = (paddleY + (paddleH / 2)) - ballPadIntersectY

        #Scale down the result
        normalizeBallPadY = ballPadRelativeY / (paddleH / 2)

        #Calculate bounce angle
        bounceAngle = normalizeBallPadY * maxBounce

        #Calculate ball speed
        ballSpeed = math.sqrt(self.infBallXVelocity**2 + self.infBallYVelocity**2)

        #Update Velocities
        self.infBallXVelocity = abs(ballSpeed) * math.cos(bounceAngle)
        self.infBallYVelocity = -abs(ballSpeed) * math.sin(bounceAngle)

    def infinite_score(self):
        self.inf_scoreFont = pg.font.SysFont("Arial", 30)

        self.inf_drawScore = self.inf_scoreFont.render(f"Score: {self.infScore}", True, (255, 255, 255))

        return self.inf_drawScore

    def infinite_level(self):
        self.inf_levelFont = pg.font.SysFont("Arial", 30)
        self.inf_drawLevel = self.inf_scoreFont.render(f"Level: {self.infLevel}", True, (255, 255, 255))      

        return self.inf_drawLevel  

    def infinite_end_game(self):
        self.inf_endGameFont = pg.font.SysFont("Arial", 30)
        self.inf_drawEnd = self.inf_endGameFont.render("Game Over!", True, (255, 255, 255))
        self.drawEndW = self.inf_drawEnd.get_width() // 2

        return self.inf_drawEnd

    def infinite_final_score(self):
        self.inf_finalScoreFont = pg.font.SysFont("Arial", 18)
        self.inf_drawFinalScore = self.inf_finalScoreFont.render(f"Final Score: {self.infScore}", True, (255, 255, 255))
        self.finalScoreW = self.inf_drawFinalScore.get_width()

        return self.inf_drawFinalScore

    def infinite_final_level(self):
        self.inf_finalLevelFont = pg.font.SysFont("Arial", 18)
        self.inf_drawFinalLevel = self.inf_finalLevelFont.render(f"Final Level: {self.infLevel}", True, (255, 255, 255))
        self.finalLevelW = self.inf_drawFinalLevel.get_width()

        return self.inf_drawFinalLevel

    def infinite_pause_options(self):
        self.inf_pauseOptionsFont = pg.font.SysFont("Arial", 18)
        self.inf_PauseOptions = self.inf_pauseOptionsFont.render("[Q] Quit | [M] Menu | [R] Restart", True, (0, 0, 0))
        self.pauseOptionsH = self.inf_PauseOptions.get_height()
        return self.inf_PauseOptions

if __name__ == "__main__":

    app = QApplication([])
    gui = pong_GUI()
    gui.show()
    app.exec()


  