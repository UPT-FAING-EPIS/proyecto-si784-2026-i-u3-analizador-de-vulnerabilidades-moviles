def pre_mutation(context):
    # Solo mutar servicios críticos para optimizar tiempo en CI
    if "services" not in context.filename:
        context.skip = True

# Ejecución: mutmut run --paths-to-mutate app/dashboard/src/controllers/