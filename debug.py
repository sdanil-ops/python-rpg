import pygame

pygame.init()
font = pygame.font.Font(None, 30)



def debug(info, y=10, x=10):

    display_surface = pygame.display.get_surface()
    # debug_surf = font.render(str(info), True, 'White')
    # debug_rect = debug_surf.get_rect(topleft=(x, y))
    # pygame.draw.rect(display_surface, 'Black', debug_rect)
    # display_surface.blit(debug_surf, debug_rect)
    for key, value in info.items():
        y += 30
        disp_surf = pygame.display.get_surface()
        text = f'{key}: {value}'
        surf = font.render(text, True, 'White')
        rect = surf.get_rect(topleft=(x, y))
        pygame.draw.rect(disp_surf, 'Black', rect)
        display_surface.blit(surf, rect)
