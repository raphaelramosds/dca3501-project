def plot_bar(ax, data, title, rotation=90, color_map=None):
    """
    Plot a bar chart given the axes
    """
    if color_map:
        if isinstance(color_map, dict):
            colors = [color_map.get(idx, 'tab:blue') for idx in data.index]
        elif callable(color_map):
            colors = [color_map(idx) for idx in data.index]
        else:
            raise ValueError("color_map deve ser um dicionário ou função.")
    else:
        colors = 'tab:blue'

    ax.bar(data.index, data.values, color=colors)
    ax.set_title(title)
    ax.set_xticks(range(len(data.index)))
    ax.set_xticklabels(data.index, rotation=rotation)