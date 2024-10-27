import customtkinter
import pygame

app = customtkinter.CTk()


app.title("my draft")
app.geometry("500x500")

def push_2048_button():
    pygame.init()
    window = pygame.display.set_mode((1000,1000))
    pos = pygame.Vector2(window.get_height()/2, window.get_width()/2)
    clock = pygame.time.Clock()
    dt = 0
    
    runing=True
    while runing:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                runing=False
        
        pygame.draw.circle(window, "red",pos, 40)
        
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            pos.y+=dt*300
        if key[pygame.K_s]:
            pos.y-=dt*300
        if key[pygame.K_a]:
            pos.x += dt*300
        if key[pygame.K_d]:
            pos.x -=dt*300
            
        pygame.display.flip()
        
        dt = clock.tick(60)/1000
            

    pygame.quit()    
    
button = customtkinter.CTkButton(app,text="2048",command=push_2048_button)
button.grid(row=100,column=0,padx=200,pady=20)




app.mainloop()

