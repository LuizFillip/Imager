def draw_labels(
        ax, 
        time, 
        date, 
        site, 
        layer,
        upper = 22,
        color = 'W'
        ):
    
    transform = ax.transAxes
    ax.text(
        0, 510, time, 
        transform = transform, 
        color = color
        )
    
    ax.text(
        395, 510, date, 
        transform = transform, 
        color = color
        )
    
    ax.text(
        0, upper, site, 
        transform = transform, 
        color = color
        )
    
    ax.text(
        480, upper, layer, 
        transform = transform, 
        color = color
        )
    
    ax.text(
        256, upper, "N", 
        transform = transform, 
        color = color
        )
    
    ax.text(
        490, 256, "E", 
        transform = transform, 
        color = color
        )
    
    
def str_time(dn):
    return dn.strftime("%H:%M:%S UT")

def str_date(dn):
    return dn.strftime("%d/%m/%Y")

def str_datetime(dn):
    return dn.strftime("%d/%m/%Y %H:%M:%S UT")
    
    
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
    
args = dict(site = 'CA', 
            date = '', 
            time = '', 
            emission = '',
            color = "black",
            upper = 22
            )    