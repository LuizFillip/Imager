
def display_image(ax_img, img, title = ''):

    ax_img.imshow(img, cmap='gray')
    ax_img.set_axis_off()
    ax_img.set(title = title)
    
    
def save_img(fig, save_in):
        
    fig.savefig(
        save_in, 
        dpi = 300, 
        pad_inches = 0, 
        bbox_inches = "tight", 
        transparent = False
        )
  
