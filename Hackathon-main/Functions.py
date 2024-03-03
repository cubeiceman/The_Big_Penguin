def in_rect(points, rectangle):
    return (rectangle.rect.x < points[0] < rectangle.rect.x + rectangle.rect.width) and (
            rectangle.rect.y < points[1] < rectangle.rect.y + rectangle.rect.height)