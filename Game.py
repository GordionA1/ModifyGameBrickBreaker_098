import tkinter as tk
import random
import math

# ==============================================================================
# Kelas Dasar (Parent Class) untuk semua objek dalam game
# ==============================================================================
class GameObject(object):
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)


# ==============================================================================
# Kelas Item Power-Up (Multiball)
# ==============================================================================
class PowerUp(GameObject):
    def __init__(self, canvas, x, y):
        self.width = 16
        self.height = 16
        self.speed = 3.5
        
        item = canvas.create_rectangle(x - self.width/2, y - self.height/2,
                                       x + self.width/2, y + self.height/2,
                                       fill='#FFCC00', outline='#FFFFFF', width=2)
        self.dot = canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill='#FF0000', outline='')
        super(PowerUp, self).__init__(canvas, item)

    def update(self):
        self.move(0, self.speed)

    def move(self, x, y):
        super(PowerUp, self).move(x, y)
        self.canvas.move(self.dot, x, y)

    def delete(self):
        super(PowerUp, self).delete()
        self.canvas.delete(self.dot)


# ==============================================================================
# Kelas Bola (Ball) - Bola Api Animasi
# ==============================================================================
class Ball(GameObject):
    def __init__(self, canvas, x, y):
        self.radius = 4 
        self.direction = [random.choice([1, -1]), -1]
        self.speed = 6.0 
        
        self.fire_outer = canvas.create_oval(x - self.radius - 4, y - self.radius - 4,
                                             x + self.radius + 4, y + self.radius + 4,
                                             fill='', outline='#FF2200', width=2)
        self.fire_mid = canvas.create_oval(x - self.radius - 2, y - self.radius - 2,
                                           x + self.radius + 2, y + self.radius + 2,
                                           fill='', outline='#FF7700', width=2)
        self.fire_inner = canvas.create_oval(x - self.radius, y - self.radius,
                                             x + self.radius, y + self.radius,
                                             fill='#FFCC00', outline='')
        item = canvas.create_oval(x - self.radius + 1, y - self.radius + 1,
                                  x + self.radius - 1, y + self.radius - 1,
                                  fill='#FFFFFF', outline='')
        super(Ball, self).__init__(canvas, item)

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if width <= 1: width = int(self.canvas['width']) 
        
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
            
        if coords[1] <= 0:
            self.direction[1] *= -1
            
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.move(x, y)

    def move(self, x, y):
        super(Ball, self).move(x, y)
        self.canvas.move(self.fire_inner, x, y)

    def animate_flames(self):
        coords = self.get_position()
        if not coords: return
        cx = (coords[0] + coords[2]) * 0.5
        cy = (coords[1] + coords[3]) * 0.5

        f1 = random.uniform(3.0, 6.0)
        self.canvas.coords(self.fire_outer, cx - self.radius - f1, cy - self.radius - f1,
                                            cx + self.radius + f1, cy + self.radius + f1)
        f2 = random.uniform(1.0, 2.5)
        self.canvas.coords(self.fire_mid, cx - self.radius - f2, cy - self.radius - f2,
                                          cx + self.radius + f2, cy + self.radius + f2)

    def delete(self):
        super(Ball, self).delete()
        self.canvas.delete(self.fire_outer)
        self.canvas.delete(self.fire_mid)
        self.canvas.delete(self.fire_inner)

    def collide(self, game_objects):
        coords = self.get_position()
        x = (coords[0] + coords[2]) * 0.5
        
        if len(game_objects) > 1:
            self.direction[1] *= -1
        elif len(game_objects) == 1:
            game_object = game_objects[0]
            coords = game_object.get_position()
            if x > coords[2]:
                self.direction[0] = 1
            elif x < coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1

        points = 0
        destroyed_coords = []
        for game_object in game_objects:
            if isinstance(game_object, Brick):
                b_coords = game_object.get_position() 
                destroyed = game_object.hit()
                points += 5
                if destroyed:
                    points += 10
                    destroyed_coords.append(b_coords) 
                    
        return points, destroyed_coords


# ==============================================================================
# Kelas Papan Pemukul (Paddle)
# ==============================================================================
class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        self.width = 120 
        self.height = 14
        self.ball = None
        
        item = canvas.create_rectangle(x - self.width/2, y - self.height/2,
                                       x + self.width/2, y + self.height/2,
                                       fill='#002244', outline='#00FFFF', width=2)
        self.core = canvas.create_rectangle(x - self.width/2 + 15, y - 3,
                                            x + self.width/2 - 15, y + 3,
                                            fill='#00FFAA', outline='')
        super(Paddle, self).__init__(canvas, item)

    def set_ball(self, ball):
        self.ball = ball

    def move(self, offset):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if width <= 1: width = int(self.canvas['width'])
            
        if coords[0] + offset < 0:
            offset = -coords[0] 
        elif coords[2] + offset > width:
            offset = width - coords[2] 
            
        if offset != 0:
            super(Paddle, self).move(offset, 0)
            self.canvas.move(self.core, offset, 0) 
            if self.ball is not None:
                self.ball.move(offset, 0)


# ==============================================================================
# Kelas Balok Bata (Brick)
# ==============================================================================
class Brick(GameObject):
    def __init__(self, canvas, x, y, hits):
        self.width = 46
        self.height = 20 
        self.hits = hits
        
        self.frame_colors = {1: '#004422', 2: '#442200', 3: '#440022'}
        self.laser_colors = {1: '#00FF55', 2: '#FF8800', 3: '#FF0055'}
        f_color = self.frame_colors.get(hits, '#444444')
        l_color = self.laser_colors.get(hits, '#FFFFFF')
        
        item = canvas.create_rectangle(x - self.width/2, y - self.height/2,
                                       x + self.width/2, y + self.height/2,
                                       fill=f_color, outline='#000000', width=1, tags='brick')
        self.glass = canvas.create_rectangle(x - self.width/2 + 4, y - self.height/2 + 4,
                                             x + self.width/2 - 4, y + self.height/2 - 4,
                                             fill='#111111', outline='')
        self.laser = canvas.create_line(x - self.width/2 + 6, y, x + self.width/2 - 6, y, fill=l_color, width=3)
        self.led1 = canvas.create_oval(x - self.width/2 + 2, y - self.height/2 + 2,
                                       x - self.width/2 + 5, y - self.height/2 + 5, fill=l_color, outline='')
        self.led2 = canvas.create_oval(x + self.width/2 - 5, y + self.height/2 - 5,
                                       x + self.width/2 - 2, y + self.height/2 - 2, fill=l_color, outline='')
        super(Brick, self).__init__(canvas, item)

    def hit(self):
        self.hits -= 1
        if self.hits <= 0:
            self.delete()
            return True
        else:
            new_f = self.frame_colors.get(self.hits, '#444444')
            new_l = self.laser_colors.get(self.hits, '#FFFFFF')
            self.canvas.itemconfig(self.item, fill=new_f)
            self.canvas.itemconfig(self.laser, fill=new_l)
            self.canvas.itemconfig(self.led1, fill=new_l)
            self.canvas.itemconfig(self.led2, fill=new_l)
            return False

    def delete(self):
        super(Brick, self).delete()
        self.canvas.delete(self.glass)
        self.canvas.delete(self.laser)
        self.canvas.delete(self.led1)
        self.canvas.delete(self.led2)


# ==============================================================================
# Kelas Utama Permainan (Game)
# ==============================================================================
class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)
        self.lives = 3
        self.score = 0
        self.level = 1
        
        self.width = 750 
        self.height = 600 
        self.frame_count = 0 
        self.game_state = 'idle' 
        
        self.canvas = tk.Canvas(self, bg='#020205', width=self.width, height=self.height, highlightthickness=0)
        self.canvas.pack()
        self.pack()

        self.ufo_parts = []
        self.ufo_lights = []
        self.sat_parts = []
        self.sat_light = None
        self.comets = []
        
        self.overlay_items = [] 

        self.draw_rich_space_background()

        self.items = {}
        self.balls = [] 
        self.powerups = []
        
        self.paddle = Paddle(self.canvas, self.width / 2, 560)
        self.items[self.paddle.item] = self.paddle

        self.hud = None
        self.score_text = None
        self.level_text = None
        
        self.keys_pressed = {'Left': False, 'Right': False}

        self.build_level()
        self.setup_game()
        
        self.canvas.focus_set()
        self.canvas.bind('<KeyPress-Left>', lambda _: self.keys_pressed.update({'Left': True}))
        self.canvas.bind('<KeyRelease-Left>', lambda _: self.keys_pressed.update({'Left': False}))
        self.canvas.bind('<KeyPress-Right>', lambda _: self.keys_pressed.update({'Right': True}))
        self.canvas.bind('<KeyRelease-Right>', lambda _: self.keys_pressed.update({'Right': False}))
        
        self.main_loop()

    def draw_rich_space_background(self):
        for _ in range(8):
            nx, ny = random.randint(0, self.width), random.randint(0, self.height)
            self.canvas.create_oval(nx, ny, nx+200, ny+150, fill='#0B0515', outline='')
        for _ in range(6):
            nx, ny = random.randint(0, self.width), random.randint(0, self.height)
            self.canvas.create_oval(nx, ny, nx+180, ny+120, fill='#05101A', outline='')

        for _ in range(180):
            x, y = random.randint(0, self.width), random.randint(0, self.height)
            size = random.choice([1, 1, 2, 2, 3])
            color = random.choice(['#FFFFFF', '#88CCFF', '#FFDD88', '#444466', '#FF99AA'])
            self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline='')

        for _ in range(12):
            ax, ay = random.randint(50, self.width-50), random.randint(150, self.height-150)
            self.canvas.create_polygon(ax, ay, ax+8, ay-5, ax+15, ay+2, ax+10, ay+10, ax+2, ay+8, 
                                       fill='#333333', outline='#222222')

        px, py = 80, 120
        self.canvas.create_line(px-50, py+25, px+100, py-25, fill='#444455', width=14, capstyle=tk.ROUND)
        self.canvas.create_oval(px, py-35, px+70, py+35, fill='#442233', outline='#663344', width=2)
        self.canvas.create_line(px-70, py+35, px+50, py-5, fill='#9988AA', width=6, capstyle=tk.ROUND)

        mx, my = 600, 80
        self.canvas.create_oval(mx, my, mx+80, my+80, fill='#882211', outline='#AA3322', width=2)
        self.canvas.create_oval(mx+20, my+30, mx+35, my+45, fill='#551100', outline='')
        self.canvas.create_oval(mx+50, my+20, mx+60, my+30, fill='#551100', outline='')
        self.canvas.create_oval(mx+40, my+60, mx+65, my+75, fill='#551100', outline='')

        jx, jy = 600, 450
        self.canvas.create_oval(jx, jy, jx+220, jy+220, fill='#051A33', outline='#113355', width=3)
        self.canvas.create_arc(jx, jy, jx+220, jy+220, start=15, extent=150, fill='#0A2244', outline='')

        sx, sy = 50, 350
        w1 = self.canvas.create_rectangle(sx, sy, sx+40, sy+15, fill='#113355', outline='#4488AA')
        w2 = self.canvas.create_rectangle(sx+70, sy, sx+110, sy+15, fill='#113355', outline='#4488AA')
        bd1 = self.canvas.create_rectangle(sx+45, sy-10, sx+65, sy+25, fill='#AAAAAA', outline='#FFFFFF')
        bd2 = self.canvas.create_rectangle(sx+48, sy-5, sx+62, sy+20, fill='#777777', outline='')
        ant = self.canvas.create_line(sx+55, sy-10, sx+55, sy-30, fill='#FFFFFF')
        self.sat_light = self.canvas.create_oval(sx+52, sy-32, sx+58, sy-26, fill='#FF0000', outline='')
        self.sat_parts.extend([w1, w2, bd1, bd2, ant, self.sat_light])

        ufo_x, ufo_y = 400, 200
        dome = self.canvas.create_oval(ufo_x+12, ufo_y, ufo_x+48, ufo_y+30, fill='#00FFAA', outline='')
        saucer = self.canvas.create_oval(ufo_x-15, ufo_y+15, ufo_x+75, ufo_y+35, fill='#222233', outline='#444455', width=2)
        self.ufo_parts.extend([dome, saucer])
        
        for lx in [ufo_x-5, ufo_x+25, ufo_x+55]:
            light = self.canvas.create_oval(lx, ufo_y+22, lx+7, ufo_y+29, fill='#FF00FF', outline='')
            self.ufo_parts.append(light)
            self.ufo_lights.append(light)

    def animate_background(self):
        self.frame_count += 1
        
        ufo_dx = 0.6 
        ufo_dy = math.sin(self.frame_count * 0.08) * 1.2 
        for part in self.ufo_parts:
            self.canvas.move(part, ufo_dx, ufo_dy)

        if self.ufo_parts:
            ufo_bbox = self.canvas.bbox(self.ufo_parts[1])
            if ufo_bbox and ufo_bbox[0] > self.width + 100:
                for part in self.ufo_parts:
                    self.canvas.move(part, -self.width - 250, 0)

        if self.frame_count % 12 == 0:
            colors = ['#FF0055', '#00FFFF', '#FFDD00', '#00FF00']
            for light in self.ufo_lights:
                self.canvas.itemconfig(light, fill=random.choice(colors))

        sat_dy = math.cos(self.frame_count * 0.04) * 0.5
        for part in self.sat_parts:
            self.canvas.move(part, 0, sat_dy)

        if self.sat_light:
            if self.frame_count % 60 < 30:
                self.canvas.itemconfig(self.sat_light, fill='#FF0000')
            else:
                self.canvas.itemconfig(self.sat_light, fill='#440000')

        if random.random() < 0.01:
            cx = random.randint(-150, self.width)
            cy = random.randint(-50, self.height // 2)
            sx = random.uniform(6, 12)
            sy = random.uniform(2, 5)
            comet = self.canvas.create_line(cx, cy, cx+30, cy+sy*4, fill='#AAFFFF', width=2, dash=(4, 4))
            self.comets.append([comet, sx, sy])

        for c in self.comets[:]:
            self.canvas.move(c[0], c[1], c[2])
            cb = self.canvas.coords(c[0])
            if cb and (cb[0] > self.width + 50 or cb[1] > self.height + 50):
                self.canvas.delete(c[0])
                self.comets.remove(c)

    def draw_hud_panel(self, title, subtitle, theme_color):
        """Membuat panel pop-up Sci-Fi Hologram dengan ukuran proporsional & rapi."""
        self.clear_overlay() 
        
        cx, cy = self.width / 2, self.height / 2
        w, h = 320, 70 # Lebar disesuaikan agar teks panjang muat sempurna
        
        bg = self.canvas.create_rectangle(cx - w, cy - h, cx + w, cy + h, fill='#03030F', outline=theme_color, width=2)
        self.overlay_items.append(bg)
        
        l_off = w - 10
        self.overlay_items.append(self.canvas.create_line(cx-l_off, cy-h+18, cx-l_off, cy-h+8, cx-l_off+30, cy-h+8, fill=theme_color, width=3))
        self.overlay_items.append(self.canvas.create_line(cx+l_off, cy-h+18, cx+l_off, cy-h+8, cx+l_off-30, cy-h+8, fill=theme_color, width=3))
        self.overlay_items.append(self.canvas.create_line(cx-l_off, cy+h-18, cx-l_off, cy+h-8, cx-l_off+30, cy+h-8, fill=theme_color, width=3))
        self.overlay_items.append(self.canvas.create_line(cx+l_off, cy+h-18, cx+l_off, cy+h-8, cx+l_off-30, cy+h-8, fill=theme_color, width=3))
        
        # Ukuran font judul disesuaikan agar muat sempurna (26pt)
        shadow = self.canvas.create_text(cx, cy - 12, text=title, font=('Consolas', 24, 'bold'), fill=theme_color)
        core = self.canvas.create_text(cx, cy - 12, text=title, font=('Consolas', 24, 'bold'), fill='#FFFFFF')
        self.overlay_items.extend([shadow, core])
        
        sub = self.canvas.create_text(cx, cy + 30, text=subtitle, font=('Consolas', 13, 'bold'), fill=theme_color)
        self.overlay_items.append(sub)

    def clear_overlay(self):
        for item in self.overlay_items:
            self.canvas.delete(item)
        self.overlay_items.clear()

    def build_level(self):
        to_delete = [item for item, obj in self.items.items() if isinstance(obj, Brick)]
        for item in to_delete:
            del self.items[item]
        self.canvas.delete('brick') 

        # Tata letak bata diatur rapi di bagian atas layar
        rows = min(4 + self.level, 8) 
        for i in range(rows):
            y = 60 + (i * 26) 
            for x in range(50, self.width - 50, 54): 
                hits = 2 if random.random() > 0.75 else 1 
                self.add_brick(x + 23, y, hits)

    def setup_game(self):
        for b in self.balls: b.delete()
        self.balls.clear()
        for p in self.powerups: p.delete()
        self.powerups.clear()
        
        self.spawn_initial_ball()
        self.update_hud()
        
        self.game_state = 'idle'
        
        title_msg = 'SYSTEM ONLINE' if self.score == 0 else 'INITIATE ROUND'
        self.draw_hud_panel(title_msg, '>> PRESS [SPACE] TO HACK <<', '#00FFFF')
        
        self.canvas.bind('<space>', lambda _: self.start_game())

    def spawn_initial_ball(self):
        paddle_coords = self.paddle.get_position()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        ball = Ball(self.canvas, x, 540)
        ball.speed = 5.0 + (self.level - 1) * 0.5
        self.paddle.set_ball(ball)
        self.balls.append(ball)

    def add_brick(self, x, y, hits):
        brick = Brick(self.canvas, x, y, hits)
        self.items[brick.item] = brick

    def trigger_multiball(self):
        new_balls = []
        for ball in self.balls:
            if len(self.balls) + len(new_balls) > 100: 
                break
            coords = ball.get_position()
            x = (coords[0] + coords[2]) * 0.5
            y = (coords[1] + coords[3]) * 0.5
            
            new_ball = Ball(self.canvas, x, y)
            new_ball.speed = ball.speed
            new_ball.direction = [random.choice([1, -1]), -1]
            new_balls.append(new_ball)
            
        self.balls.extend(new_balls)

    def draw_text(self, x, y, text, size=24, weight='bold', fill_color='#00FFFF'):
        font = ('Consolas', size, weight)
        return self.canvas.create_text(x, y, text=text, font=font, fill=fill_color)

    def update_hud(self):
        lives_txt = f'LIVES: {self.lives}'
        score_txt = f'SCORE: {self.score}'
        level_txt = f'LEVEL: {self.level}'
        
        if self.hud is None:
            self.hud = self.draw_text(70, 20, lives_txt, 13, 'bold')
            self.score_text = self.draw_text(self.width/2, 20, score_txt, 13, 'bold')
            self.level_text = self.draw_text(self.width - 70, 20, level_txt, 13, 'bold')
        else:
            self.canvas.itemconfig(self.hud, text=lives_txt)
            self.canvas.itemconfig(self.score_text, text=score_txt)
            self.canvas.itemconfig(self.level_text, text=level_txt)

    def start_game(self):
        self.canvas.unbind('<space>')
        self.clear_overlay() 
        self.paddle.ball = None
        self.game_state = 'playing'

    def main_loop(self):
        self.animate_background()
        
        for ball in self.balls:
            ball.animate_flames()

        if self.game_state == 'playing':
            if self.keys_pressed['Left']: self.paddle.move(-12) 
            if self.keys_pressed['Right']: self.paddle.move(12)
                
            num_bricks = len(self.canvas.find_withtag('brick'))
            
            if num_bricks == 0: 
                self.level += 1
                self.score += 2000 
                self.update_hud()
                
                self.draw_hud_panel('SECTOR CLEARED', 'INITIALIZING NEXT NODE...', '#00FF55')
                self.game_state = 'transition'
                self.after(2000, self.next_level)
                return
                
            for ball in self.balls[:]:
                if ball.get_position()[3] >= self.height: 
                    ball.delete()
                    self.balls.remove(ball)
                else:
                    ball.update()
                    self.check_collisions(ball)

            if len(self.balls) == 0:
                self.lives -= 1
                if self.lives < 0: self.lives = 0
                self.keys_pressed = {'Left': False, 'Right': False} 
                self.update_hud()
                
                if self.lives == 0:
                    self.draw_hud_panel('GAME OVER', f'FINAL SCORE: {self.score}', '#FF0033')
                    self.game_state = 'game_over'
                else:
                    self.game_state = 'transition'
                    self.after(1000, self.setup_game)
                return

            for pu in self.powerups[:]:
                pu.update()
                coords = pu.get_position()
                
                if coords[3] >= self.height:
                    pu.delete()
                    self.powerups.remove(pu)
                else:
                    overlap = self.canvas.find_overlapping(*coords)
                    if self.paddle.item in overlap:
                        self.trigger_multiball() 
                        self.score += 50
                        self.update_hud()
                        pu.delete()
                        self.powerups.remove(pu)

        self.after(16, self.main_loop)

    def check_collisions(self, ball):
        ball_coords = ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        
        points, destroyed_coords = ball.collide(objects)
        
        if points > 0:
            self.score += points
            self.update_hud()
            
        for b_coords in destroyed_coords:
            if random.random() < 0.15 and len(b_coords) == 4: 
                bx = (b_coords[0] + b_coords[2]) / 2
                by = (b_coords[1] + b_coords[3]) / 2
                pu = PowerUp(self.canvas, bx, by)
                self.powerups.append(pu)

    def next_level(self):
        self.keys_pressed = {'Left': False, 'Right': False}
        self.clear_overlay() 
        self.build_level()
        self.setup_game()


# ==============================================================================
# Titik Masuk Utama Program (Main Execution)
# ==============================================================================
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Animated Space Fireball Breaker')
    root.resizable(False, False) 
    root.configure(bg='#020205') 
    game = Game(root)
    game.mainloop()