import zipfile
from io import BytesIO

from behave import given, then, when

from app.dashboard.services.apk_analyzer import ApkAnalyzer


@given("que el usuario inicio sesion")
def step_user_logged_in(context):
    context.user = {"id": "user-1", "username": "demo"}


@when("sube un archivo APK valido")
def step_upload_valid_apk(context):
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as apk_zip:
        apk_zip.writestr("AndroidManifest.xml", "<manifest />")
        apk_zip.writestr("classes.dex", b"dex\n035")
    context.apk_bytes = buffer.getvalue()


@when("presiona el boton de analizar")
def step_press_analyze(context):
    context.result = ApkAnalyzer().analyze(context.apk_bytes)


@then("el sistema registra el escaneo")
def step_scan_is_registered(context):
    assert context.result.status == "completed"


@then("muestra los hallazgos encontrados")
def step_findings_are_visible(context):
    assert context.result.summary


@when("intenta analizar un archivo que no es APK")
def step_upload_invalid_file(context):
    context.result = ApkAnalyzer().analyze(b"archivo-invalido")


@then("el sistema rechaza el archivo")
def step_rejects_file(context):
    assert context.result.status == "failed"


@then("muestra un mensaje de error claro")
def step_error_is_clear(context):
    assert "APK valido" in context.result.summary
