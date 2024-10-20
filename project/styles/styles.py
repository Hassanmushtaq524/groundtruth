import reflex as rx

custom_theme = rx.theme(
        fonts={
            "heading": "Helvetica Neue LT Std, sans-serif",
            "body": "Helvetica Neue LT Std, sans-serif",
        },
        font_sizes={
            "xs": "12px",
            "sm": "14px",
            "md": "16px",
            "lg": "18px",
            "xl": "24px",
            "2xl": "30px",
            "3xl": "36px",
            "4xl": "48px",
            "5xl": "64px",
            "6xl": "80px",
        },
        colors={
            "primary": "#C48DFF",
            "secondary": "#A76FE3",
            "background": "white",
            "text": "black",
        },
        text_styles={
            "heading": {
                "font_family": "heading",
                "font_weight": "bold",
                "line_height": "1.2",
            },
            "body": {
                "font_family": "body",
                "line_height": "1.5",
            },
        },
    )
