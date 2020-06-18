"""Compile static assets."""
from flask import current_app as app
from flask_assets import Bundle

def compile_static_assets(assets):
    """Configure and build asset bundles."""
    """Configure and build asset bundles."""
    assets.debug = False

    # Stylesheets Bundles
    main_style_bundle = Bundle('src/less/*.less',
                               'main_bp/homepage.less',
                               filters='less,cssmin',
                               output='dist/css/landing.css',
                               extra={'rel': 'stylesheet/css'})

    auth_style_bundle = Bundle('src/less/*.less',
                               'auth_bp/account.less',
                                filters='less,cssmin',
                                output='dist/css/aulanding.css',
                                extra={'rel': 'stylesheet/less'})

    admin_style_bundle = Bundle('src/less/*.less',
                                filters='less,cssmin',
                                output='dist/css/admlanding.css',
                                extra={'rel': 'stylesheet/less'})

    # Register assets
    assets.register('main_styles', main_style_bundle)
    assets.register('auth_styles', auth_style_bundle)
    assets.register('admin_styles', admin_style_bundle)

    # Build assets
    if app.config['FLASK_ENV'] == 'development':  # Only rebuild bundles in development
        main_style_bundle.build()
        auth_style_bundle.build()
        admin_style_bundle.build()

    return assets
