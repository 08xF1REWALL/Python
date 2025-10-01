from functools import partial

# Simple HTML tag generator function
def tag(name, **attributes):
    attr_str = ' '.join(f'{key if key != "cls" else "class"}="{value}"'
                        for key, value in attributes.items())
    return f'<{name} {attr_str} />'

# Create a partial function for image tags with a preset class
picture = partial(tag, 'img', cls='pic-frame')

# Use the partial function
print(picture(src='wumpus.jpeg'))
