# voir: https://stackoverflow.com/q/26892392
# pour l'animation.

import numpy as np
import matplotlib.axes as ax
from typing import Tuple, List, Callable


class ScatterAnimationFigure:

    s_c1 = [0, 0, 0.5]
    s_c2 = [1, 0, 0  ]

    @staticmethod
    def get_point_values(f: Callable[[np.ndarray], float],
                   get_next_x: Callable[[np.ndarray], np.ndarray],
                   x_0: np.ndarray,
                   n: int) \
            -> Tuple[np.ndarray, np.ndarray]:
        # hack to always have an array.
        x_0 = np.array(x_0, dtype=float)
        x = x_0
        l = 1 if len(x.shape) == 0 else x.shape[0]
        points = np.empty(shape=(n, l))
        values = np.empty(shape=(n, 1))
        for i in range(n):
            points[i] = x
            values[i] = f(x)
            x = get_next_x(x)
        return points, values

    def __init__(self, points: np.ndarray, values: np.ndarray, c1=None, c2=None):
        self.points = points
        self.values = values
        self.scat = None

        if c1 is None:
            c1 = self.s_c1
        if c2 is None:
            c2 = self.s_c2
        self.c1 = np.array(c1)
        self.c2 = np.array(c2)

    def _animate(self, axes: ax.Axes, s: int) -> None:
        def get_colours(c1: np.array, c2: np.array, n: int) -> List[np.array]:
            nu = np.arange(0, 1, 1/n)
            cs = [np.empty(3)] * n
            for i in range(n):
                cs[i] = c1 + (c2 - c1) * nu[i]
            return cs

        number_frames = len(self.points)

        colours = get_colours(self.c1, self.c2, number_frames)
        # the below plots us (x0, x1) when in R2, and (x, y) otherwise.
        y = self.values if self.points.shape[1] == 1 else self.points[:, 1]
        self.scat = axes.scatter(
            self.points[:, 0],
            y,
            s=s,
            c=colours,
            marker='x'
        )

        """
        def init():
            self.scat.set_offsets(np.empty(shape=(0, 2)))
            return self.scat,

        def get_next_point(i: int):
            print(self.points[i])
            self.scat.set_offsets(self.points[:i])
            return self.scat,


        self.anim = animation.FuncAnimation(
            axes.figure,
            get_next_point,
            init_func=init,
            frames=number_frames,
            interval=self.interval,
            blit=False,
            repeat=self.repeat
            )
        """

    def plot(self, axes: ax.Axes, s: int = 50) -> None:
        self._animate(axes, s)
