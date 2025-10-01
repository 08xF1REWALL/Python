def clip(text, max_len=80):
    """Return text clipped at the last space before or after max_len."""
    end = None                                # default: “no cut yet”

    if len(text) > max_len:                  # only bother if it’s too long
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:                # found a space before the limit
            end = space_before
        else:                                # no space before; try after
            space_after = text.find(' ', max_len)   # use find, not rfind
            if space_after >= 0:
                end = space_after

    if end is None:                          # still nothing? use full length
        end = len(text)

    return text[:end].rstrip()               # final clipped string

print(clip("The quick brown fox jumps over the lazy dog", 20))  # Expect: 'The quick brown fox'
print(clip("HelloWorldWithoutSpaces", 10))                      # Expect: 'HelloWorldWithoutSpaces'
print(clip("One two three four five six", 10))                  # Expect: 'One two'
