from manim import *
import itertools as it


class Intent2(VMobject):
    CONFIG = {
        'my_zero': 0,
        'max_ratio_shown': .7,  # esto define el largo del arco
        'frequency': .2,  # la cantidad de veces que se repite
        'use_copy': True
    }

    def __init__(self, template, **kwargs):
        VMobject.__init__(self, **kwargs)
        if self.CONFIG['use_copy'] is False:
            self.ghost_mob = template.copy().fade(1)
            self.add(self.ghost_mob)
        else:
            self.ghost_mob = template
        self.shown_mob = template.copy()
        self.shown_mob.clear_updaters()
        self.add(self.shown_mob)

        def update(mob, dt):
            mob.CONFIG['my_zero'] += dt
            period = 10/mob.CONFIG['frequency']
            unsmooth_alpha = (mob.CONFIG['my_zero'] % period)/period
            alpha = bezier([0, 1, 0, 1])(unsmooth_alpha)
            mrs = mob.CONFIG['max_ratio_shown']
            mob.shown_mob.pointwise_become_partial(
                mob.ghost_mob,
                max(interpolate(-mrs, 1, alpha), 0),
                min(interpolate(0, 1+mrs, alpha), 1)
            )
        self.add_updater(update)


class Trying2(Scene):
    CONFIG = {
        'colors': [
            RED, GREEN, BLUE, YELLOW
        ]
    }

    def construct(self):
        radios = [t for t in np.linspace(0, 3, 20)]
        arcs = VGroup()
        my_color = it.cycle(self.CONFIG['colors'])
        for radio in radios:
            arc = Arc(start_angle=0, angle=2*PI, radius=radio, stroke_width=2)
            # se puede colocar aca como dentro del mismo VMobject
            arc.set_color(color=next(my_color))
            my_intent = Intent2(arc)
            arcs.add(my_intent)
        self.add(arcs)
        self.wait(10)
