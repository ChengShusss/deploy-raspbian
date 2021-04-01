# ------------------------------------------
# @Author: Cheng Shu
# @Date: 2021-02-05 16:05:55
# @LastEditTime: 2021-02-06 17:16:42
# @LastEditors: Cheng Shu
# @Description: simplified example/graph.py to find how to use BarGraph.
# @FilePath: \curses\testGraph.py
# @@Copyright © 2020 Cheng Shu
# ------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python
#
# Urwid graphics example program
#    Copyright (C) 2004-2011  Ian Ward
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Urwid web site: http://excess.org/urwid/

"""
Urwid example demonstrating use of the BarGraph widget and creating a
floating-window appearance.  Also shows use of alarms to create timed
animation.
"""

import urwid
import time
import asyncio


class GraphView(urwid.WidgetWrap):
    """
    A class responsible for providing the application's interface and
    graph display.
    """
    palette = [
        ('bg background', 'light gray', 'black'),
        ('bg 1',         'black',      'dark blue'),
        ('bg 2',         'black',      'dark cyan', 'standout'),
        ('bg 3',         'black',      'light gray', 'standout'),
        ('leftBody', 'light cyan', 'black'),
    ]

    def __init__(self):
        self.graph = urwid.BarGraph(['bg background', 'bg 2', 'bg 3', 'bg 1'])
        self.graph_wrap = urwid.WidgetWrap(self.graph)
        vline = urwid.AttrWrap(urwid.SolidFill(u'\u2502'), 'line')

        blank = urwid.Divider()
        left_listbox_content = [
            urwid.Text("BlockChain Height:"),
            urwid.Text("10", align='center'),
            blank,
            urwid.Text("Lash Block:"),
            urwid.Text("cd94f7b8a31cd878490bfc1", align='center'),
            blank,
            urwid.Text("Tx pool:"),
            urwid.Text("10 Tx in pool", align='center'),
            blank,
            urwid.Text("Null"),
            blank,
            urwid.Text("Reserved Positon")
        ]
        leftContent = urwid.AttrWrap(urwid.ListBox(
            urwid.SimpleListWalker(left_listbox_content)), 'leftBody')

        w = urwid.Columns([leftContent,
                           ('fixed', 1, vline),
                           self.graph_wrap])
        self.graph.set_data([[9.0, 0], [0, 29.0], [49.0, 0], [
                            0, 69.0], [89.0, 0], [69.0, 0], [9.0, 0], [0, 29.0], [49.0, 0], [
            0, 69.0], [89.0, 0], [69.0, 0]], 100)

        frame = urwid.Frame(w)

        self.loop = urwid.MainLoop(frame, self.palette)
        # self.loop.run()

    async def start(self):
        with self.loop.start():
            while 1:
                self.loop.draw_screen()
                await asyncio.sleep(1)


if '__main__' == __name__:
    asyncio.run(GraphView().start())
    # GraphView()
