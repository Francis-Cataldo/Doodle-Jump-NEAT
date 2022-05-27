import pygame as pg
import random
from settings import *
from sprites import *
from os import path
import neat
import numpy as np
import matplotlib.pyplot as plt
import visualize
import pickle



recording = False
best_net_fit = 0
best_net = None


def run_nets(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    winner = p.run(eval_genomes, 100)

    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    # Create NN visualization for best performer over all generations
    node_names = {-1:'Player X Position', -2: 'Platform X Position', -3: 'Player X Velocity', 0:'Movement Direction'}
    visualize.draw_net(config, best_net, True, node_names=node_names)
    
    with open('best_net.pickle', 'wb') as f:
        pickle.dump(best_net, f, protocol=pickle.HIGHEST_PROTOCOL)

    # create plots of avg. fitness, best fitness, and speciation... display
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    plt.show()

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    p.run(eval_genomes, 10)

def run_best_net(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    # opens best net from save
    genome = None
    with open('best_net.pickle', 'rb') as f:
        genome = pickle.load(f)
    
    nets = []
    ge = []
    players = []
    g = Game(nets, ge, players)

    # adds net to the game
    nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
    ge.append(genome)
    player = Player(g)
    players.append(player)
    g.all_sprites.add(player)

    

    g.run()

def eval_genomes(genomes, config):
    nets = []
    ge = []
    players = []
    
    g = Game(nets, ge, players) # pass by reference allows players to be created after game

    for genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome[1], config)

        nets.append(net)
        player = Player(g)
        players.append(player)

        genome[1].fitness = 0
        ge.append(genome[1])

    g.all_sprites.add([player for player in g.players])
    
    # main game loop
    g.run()

    pg.quit()
    del g
    del genomes
    del nets
    del ge
    del players
     

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        pg.display.set_icon(ICON)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def __init__(self, nets, ge, players):
        self.nets = nets
        self.ge = ge
        self.players = players

        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        pg.display.set_icon(ICON)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

        self.score = 0
        # game made harder when reaching these scores
        self.score_boundaries = [400, 600, 800, 1200, 2000, 2800, 3600, 4400, 5200]
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.num_of_platforms = NUMBER_OF_PLATFORMS

        self.all_sprites.add([player for player in self.players])
        self.initial_platform = Platform(*INITIAL_PLATFORM)
        self.all_sprites.add(self.initial_platform)
        self.platforms.add(self.initial_platform)
        self.initial_platform.moving_chance = 0
        self.initial_platform.dangerous_chance = 0
        PLATFORMS = []

        # add platforms to PLATFORMS list
        for i in range(NUMBER_OF_PLATFORMS):
            plat = (random.randrange(0, WIDTH - PLATFORM_WIDTH),
                    random.randrange(0, HEIGHT))
            PLATFORMS.append(plat)

        for plat in PLATFORMS:
            p = Platform(*plat)
            # make sure none of the initial platforms are dangerous
            if p.dangerous_chance == 1:
                p.image = pg.image.load(os.path.join('img', 'green_grass_platform.png'))
                p.dangerous_chance = 0
            self.all_sprites.add(p)
            self.platforms.add(p)

        pg.mixer.music.load(path.join(self.sound_dir, 'playing.ogg'))   # loads gameplay music
        self.max_fitnesses_not_recorded = True

        # self.run()

    # loads high score and sounds
    def load_data(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'w+') as f:
            try:
                self.highscore = int(f.read())
            except ValueError:
                self.highscore = 0
        self.sound_dir = path.join(self.dir, 'sound')    # point sound_dir to sound directory
        self.jump_sound = pg.mixer.Sound(path.join(self.sound_dir, 'jumping.wav'))
        self.blueplat_sound = pg.mixer.Sound(path.join(self.sound_dir, 'blueplat.wav'))
        self.death_sound = pg.mixer.Sound(path.join(self.sound_dir, 'death.wav'))
       
    # new game
    def new(self):
        self.score = 0
        # game made harder when reaching these scores
        self.score_boundaries = [400, 600, 800, 1200, 2000, 2800, 3600, 4400, 5200]
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.num_of_platforms = NUMBER_OF_PLATFORMS

        self.all_sprites.add([player for player in self.players])
        self.initial_platform = Platform(*INITIAL_PLATFORM)
        self.all_sprites.add(self.initial_platform)
        self.platforms.add(self.initial_platform)
        self.initial_platform.moving_chance = 0
        self.initial_platform.dangerous_chance = 0
        PLATFORMS = []

        # add platforms to PLATFORMS list
        for i in range(NUMBER_OF_PLATFORMS):
            plat = (random.randrange(0, WIDTH - PLATFORM_WIDTH),
                    random.randrange(0, HEIGHT))
            PLATFORMS.append(plat)

        for plat in PLATFORMS:
            p = Platform(*plat)
            # make sure none of the initial platforms are dangerous
            if p.dangerous_chance == 1:
                p.image = pg.image.load(os.path.join('img', 'green_grass_platform.png'))
                p.dangerous_chance = 0
            self.all_sprites.add(p)
            self.platforms.add(p)

        pg.mixer.music.load(path.join(self.sound_dir, 'playing.ogg'))   # loads gameplay music
        
        self.run()            

    # game running loop
    def run(self):
        pg.mixer.music.play(loops=-1)       # loops music until run ends
        self.playing = True
        frame = 0
        while self.playing:
            # print(len(self.players))
            self.clock.tick(FPS)
            self.events()
            self.update(frame)
            self.draw()
            frame += 1
            frame %= 10
        pg.mixer.music.fadeout(30)

    # update all sprites
    def update(self, frame):
        self.all_sprites.update()
        player_with_max_height = None
        try:
            player_with_max_height = self.players[0] # max height is lowest because of window bounds
        except:
            pass
        
        # plat_tuple = ()
        # counter = 0
        # for plat in self.platforms:
        #     if counter < 10:
        #         plat_tuple += (plat.rect.x + plat.rect.width/2,)
        #     counter += 1

        for i in range(len(self.players)):
            if self.players[i].pos.x > WIDTH:
                self.players[i].pos.x = 0
                self.ge[i].fitness -= .2
            if self.players[i].pos.x < 0:
                self.players[i].pos.x = WIDTH
                self.ge[i].fitness -= .2

            if self.players[i].vel.y > 10:
                self.ge[i].fitness += 5

            closest_platform = 0, None
            
            for p in self.platforms:
                # compute the closest platform based purely on x position... pass it into corresponding neural network
                if (closest_platform[1] == None):
                    closest_platform = abs(p.rect.x + p.rect.width/2 - self.players[i].rect.x + self.players[i].rect.width/2), p
                else:
                    if p.rect.y > self.players[i].rect.y:
                        dist = abs(p.rect.x + p.rect.width/2 - (self.players[i].rect.x + self.players[i].rect.width/2))
                                
                        if dist < closest_platform[0]:
                            closest_platform = dist, p

            input = (self.players[i].rect.x + self.players[i].rect.width/2, closest_platform[1].rect.x + closest_platform[1].rect.width/2)

            global recording
            if (recording):
                # print("playerX = " + str(self.players[i].rect.x + self.players[i].rect.width/2) + ", closestPlatX = " + str(closest_platform[1].rect.x + closest_platform[1].rect.width/2))
                pass

                      

            self.players[i].bounce()
            if self.players[i].rect.y < player_with_max_height.rect.y:
                player_with_max_height = self.players[i]

            # activate net
            output = self.nets[i].activate(input)  

            # interpret output. If < .5, move to the right, else, move to the left
            if output[0] > .5:
                self.players[i].acc.x = PLAYER_ACC
            else:
                self.players[i].acc.x = -PLAYER_ACC

            self.ge[i].fitness += .1

            if self.players[i].rect.y > 350:
                self.ge[i].fitness -= .05

        #creep to avoid halting in training
        creep_per_10_frames = 1 # must be an int
        if (frame % 10 == 0):
            for player in self.players:
                player.pos.y += creep_per_10_frames
            for plat in self.platforms:
                plat.rect.y += creep_per_10_frames
                if plat.rect.y >= HEIGHT:     
                        plat.kill()
                        self.platforms.remove(plat)
                        del plat
                        self.score += 10

        # scroll based on highest player
        if player_with_max_height != None:
            if player_with_max_height.rect.y <= HEIGHT * 1/8: # was 1/3
                for player in self.players:
                    player.pos.y += abs(player_with_max_height.vel.y)
                for plat in self.platforms:
                    plat.rect.y += abs(player_with_max_height.vel.y)
                    if plat.rect.y >= HEIGHT:     
                        plat.kill()
                        self.platforms.remove(plat)
                        del plat
                        self.score += 10    # increment score when platform is killed

        # regenerate the platforms that have been destroyed
        while len(self.platforms) < self.num_of_platforms:
            p = Platform(random.randrange(0, WIDTH - PLATFORM_WIDTH),
                         -random.randrange(0, int(HEIGHT * 1/3)))
            self.platforms.add(p)
            self.all_sprites.add(p)

        # game over condition
        i = 0
        for player in self.players:
            if player.rect.bottom > HEIGHT:
                self.players.remove(player)
                del self.nets[i]
                del self.ge[i]
            i += 1
        
        # save the best player from each generation... compare to the higher one previously and save the highest one
        global best_net_fit, best_net
        if len(self.players) == 1:
            if self.ge[0].fitness > best_net_fit:
                best_net_fit = self.ge[0].fitness
                best_net = self.ge[0]
            recording = True
        
        # game over... prepare for the next generation
        if len(self.players) == 0:
            # print("no players left")
                
            self.playing = False
            recording = False

        if len(self.platforms) == 0:   # end game when there are no more platforms
            self.playing = False
            self.death_sound.play()
            pg.mixer.music.fadeout(100)

    # check for exit condition           
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    # draw sprites to screen using image for surface and rect for location
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        

    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


if __name__ == "__main__":
    try:
        choice = int(input("Train(1), Run best net(2)"))
    except:
        exit()
    if (choice == 1):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config-feedforward')
        run_nets(config_path)
    elif (choice == 2):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config-feedforward')
        run_best_net(config_path)
    
    
