def post_init_hook(env):
    env['crm.lead']._ets_after_module_update()
