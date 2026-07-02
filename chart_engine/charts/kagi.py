# chart_engine/charts/kagi.py
from matplotlib.ticker import FuncFormatter
from matplotlib.collections import LineCollection
class Kagi:

    @staticmethod
    def floor_in_steps(number, step):
        return number // step * step

    @staticmethod
    def get_steps_rounded_coordinates(input_data, step):

        normalised_data = [
            (
                element[0],
                Kagi.floor_in_steps(
                    element[1],
                    step
                )
            )
            for element in input_data
        ]

        return normalised_data

    @staticmethod
    def get_colors(kagi_data):

        values = [price for _, price in kagi_data]

        colors = []

        if len(values) < 3:
            return [("green", values[0], "green")] * len(values)

        current_color = "green"

        for i in range(len(values)):

            if i < 2:
                colors.append(
                    (
                        current_color,
                        values[i],
                        current_color
                    )
                )
                continue

            v = values[i]
            v1 = values[i - 1]
            v2 = values[i - 2]

            if v > v1 and v > v2:

                if current_color != "green":
                    current_color = "green"

                    value = (
                        "red",
                        v2,
                        "green"
                    )

                else:

                    value = (
                        current_color,
                        v2,
                        current_color
                    )

            elif v < v1 and v < v2:

                if current_color != "red":
                    current_color = "red"

                    value = (
                        "green",
                        v2,
                        "red"
                    )

                else:

                    value = (
                        current_color,
                        v2,
                        current_color
                    )

            else:

                value = (
                    current_color,
                    (v1 + v) / 2,
                    current_color
                )

            colors.append(value)

        return colors

    @staticmethod
    def get_kagi_coordinates(input_data):

        to_be_deleted_indexes = []

        data_to_return = input_data[:]

        if len(input_data) < 2:
            return data_to_return

        for i in range(1, len(data_to_return)):
            if data_to_return[i-1][1] == data_to_return[i][1]:
                to_be_deleted_indexes.append(i)

        for i in range(len(to_be_deleted_indexes) - 1, -1, -1):
            del data_to_return[to_be_deleted_indexes[i]]

        
        to_be_deleted_indexes = []

        for i in range(1, len(data_to_return)-1):
            if data_to_return[i - 1][1] > data_to_return[i][1] > data_to_return[i + 1][1]:

                to_be_deleted_indexes.append(i)

            elif data_to_return[i - 1][1] < data_to_return[i][1] < data_to_return[i + 1][1]:

                to_be_deleted_indexes.append(i)
        

        for i in range(len(to_be_deleted_indexes) - 1, -1, -1):
            del data_to_return[to_be_deleted_indexes[i]]
        
        return data_to_return

    @staticmethod
    def get_plot_coordinates(kagi_data):

        x = list(range(len(kagi_data)))

        y = [
            price
            for _, price in kagi_data
        ]

        return x, y

    @staticmethod
    def plot_kagi_chart(ax, kagi_data, linewidth=1,
        title="Kagi Chart", xlabel="Bars", ylabel="Price",
        show_grid=True, grid_alpha=0.3, y_axis_right=True,
        y_padding=0.02,):


        x, y = Kagi.get_plot_coordinates(kagi_data)
        colors = Kagi.get_colors(kagi_data)

        segments = []
        seg_colors = []

        # --------------------------------------------------------
        # BUILD SEGMENTS (FAST PART)
        # --------------------------------------------------------
        for i in range(len(y) - 1):

            # horizontal segment
            segments.append([
                (x[i], y[i]),
                (x[i + 1], y[i])
            ])
            seg_colors.append(colors[i][2])

            if i != 0:

                # swing change
                if colors[i + 1][0] != colors[i + 1][2]:

                    segments.append([
                        (x[i + 1], y[i]),
                        (x[i + 1], colors[i + 1][1])
                    ])
                    seg_colors.append(colors[i + 1][0])

                    segments.append([
                        (x[i + 1], colors[i + 1][1]),
                        (x[i + 1], y[i + 1])
                    ])
                    seg_colors.append(colors[i + 1][2])

                # no swing change (simple vertical)
                else:
                    segments.append([
                        (x[i + 1], y[i]),
                        (x[i + 1], y[i + 1])
                    ])
                    seg_colors.append(colors[i + 1][0])

        # --------------------------------------------------------
        # SINGLE DRAW CALL (THIS IS THE SPEED BOOST)
        # --------------------------------------------------------
        lc = LineCollection(segments, colors=seg_colors, linewidths=linewidth)
        ax.add_collection(lc)

        # --------------------------------------------------------
        # STYLING (UNCHANGED)
        # --------------------------------------------------------
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        if show_grid:
            ax.grid(True, alpha=grid_alpha)

        if y_axis_right:
            ax.yaxis.tick_right()
            ax.yaxis.set_label_position("right")

        ax.set_xlim(x[0], x[-1])

        ax.set_ylim(
            min(y) * (1 - y_padding),
            max(y) * (1 + y_padding)
        )

        # --------------------------------------------------------
        # DATE LABELS (KEEP YOUR CURRENT LOGIC)
        # --------------------------------------------------------
        def format_date(x_value, pos):
            index = int(round(x_value))
            if 0 <= index < len(kagi_data):
                dt = kagi_data[index][0]
                return dt.strftime("%Y-%m-%d")
            return ""

        ax.xaxis.set_major_formatter(FuncFormatter(format_date))

    @staticmethod
    def plot_simple(
        symbol="BTC-USD",
        days=2000,
        step=500,
        ax=None,
        figsize=(12, 6),
        linewidth=1,

        # data overrides (optional)
        raw_data=None,
        kagi_data=None,

        # styling passthrough
        title="Kagi Chart",
        xlabel="Bars",
        ylabel="Price",
        show_grid=True,
        grid_alpha=0.3,
        y_axis_right=True,
        y_padding=0.02,
    ):
        import matplotlib.pyplot as plt
        from chart_engine.data_scraping.data import YahooData

        # --------------------------------------------------------
        # AX CREATION
        # --------------------------------------------------------
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig = ax.figure

        # --------------------------------------------------------
        # DATA PIPELINE
        # --------------------------------------------------------
        if kagi_data is None:
            if raw_data is None:
                raw_data = YahooData.get_yahoo_closes(symbol, days)

            rounded = Kagi.get_steps_rounded_coordinates(raw_data, step)
            kagi_data = Kagi.get_kagi_coordinates(rounded)

        # --------------------------------------------------------
        # DELEGATE PLOTTING
        # --------------------------------------------------------
        Kagi.plot_kagi_chart(
            ax,
            kagi_data,
            linewidth=linewidth,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            show_grid=show_grid,
            grid_alpha=grid_alpha,
            y_axis_right=y_axis_right,
            y_padding=y_padding,
        )

        return fig, ax