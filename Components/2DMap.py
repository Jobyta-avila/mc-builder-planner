def draw_grid():
    for x in range(0, 800, 20):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, 600))
    for y in range(0, 600, 20):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (800, y))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255, 255, 255))
    draw_grid()
    pygame.display.flip()
    pygame.time.wait(10)
