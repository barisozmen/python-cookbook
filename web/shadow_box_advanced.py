
# Taken from https://www.joshwcomeau.com/shadow-palette/ and picked the light position with coordinates x=-1, y=2
def box_shadow_advanced(color, elevation):
    shadowified_color = f'hsl({color.replace(",", "").lstrip("hsl(").rstrip(")")} / 0.34)' # TODO: later improve it by hsl colors as in https://www.joshwcomeau.com/shadow-palette/, and also learn the hsl color concept from https://www.joshwcomeau.com/css/color-formats/
    elevation_dict = {
        'low': f'''
            0.2px 0.3px 0.4px {shadowified_color},
            0.3px 0.5px 0.7px -1.2px {shadowified_color},
            0.7px 1.2px 1.6px -2.5px {shadowified_color};
        ''',
        'medium': f'''
            0.2px 0.3px 0.4px {shadowified_color},
            0.6px 1px 1.3px -0.8px {shadowified_color},
            1.4px 2.5px 3.2px -1.7px {shadowified_color},
            3.4px 6.2px 8px -2.5px {shadowified_color};
        ''',
        'high': f'''
            0.2px 0.3px 0.4px {shadowified_color},
            1px 1.8px 2.3px -0.4px {shadowified_color},
            1.9px 3.4px 4.4px -0.7px {shadowified_color},
            3.1px 5.5px 7.1px -1.1px {shadowified_color},
            4.9px 8.8px 11.3px -1.4px {shadowified_color},
            7.7px 13.8px 17.8px -1.8px {shadowified_color},
            11.6px 21px 27px -2.1px {shadowified_color},
            17.1px 30.9px 39.7px -2.5px {shadowified_color};
        '''
    }
    return f'box-shadow: {elevation_dict[elevation]}'