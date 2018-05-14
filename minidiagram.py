import base64
import io
import random
import cairo

class MiniDiagram():
    def __init__(self, *, bgcolor=(1,1,1), width=80, height=20):
        self.bgcolor = bgcolor
        self.width = width
        self.height = height
        self.data = []

    def add_data(self, row, color):
        self.data.append((row, color))

    def get_data_uri(self):
        png = self.make()
        b64 = base64.b64encode(png).decode()
        return 'data:image/png;base64,{b64}'.format(b64=b64)

    def make(self):
        with cairo.ImageSurface(cairo.Format.ARGB32, self.width, self.height) as surface:
            context = cairo.Context(surface)
            self.draw_background(context)
            for row, color in self.data:
                self.draw_data(context, row, color)
            with io.BytesIO() as png_file_contents:
                surface.write_to_png(png_file_contents)
                return png_file_contents.getvalue()

    def draw_background(self, context):
        context.set_source_rgba(*self.bgcolor, 0.6)
        context.rectangle(0.5, 0, self.width - 1, self.height)
        context.fill()

        context.set_source_rgba(*self.bgcolor, 1)
        context.set_line_width(1)
        context.move_to(0, 0.5)
        context.line_to(self.width, 0.5)
        context.move_to(0, self.height - 0.5)
        context.line_to(self.width, self.height - 0.5)
        context.stroke()

    def draw_data(self, context, row, color):
        lenrow = len(row)
        maxrow = max(row)
        minrow = min(row)
        xs = [self.width - 0.5 - (i * (self.width - 1) / (lenrow - 1)) for i in range(0, lenrow)]
        ys = [self.height - ((val - minrow) / (maxrow - minrow) * self.height) for val in row] 

        # fill area under line graph
        context.set_source_rgba(*color, 0.6)
        context.move_to(0.5, self.height)
        context.line_to(self.width - 0.5, self.height)
        for i in range(0, lenrow):
            context.line_to(xs[i], ys[i])
        context.close_path()
        context.fill()

        # make line graph
        context.set_source_rgba(*color, 1)
        context.set_line_width(1)
        context.set_line_cap(cairo.LineCap.ROUND)
        context.set_line_join(cairo.LineJoin.ROUND)
        context.move_to(xs[0], ys[0])
        for i in range(1, lenrow):
            context.line_to(xs[i], ys[i])
        context.stroke()
