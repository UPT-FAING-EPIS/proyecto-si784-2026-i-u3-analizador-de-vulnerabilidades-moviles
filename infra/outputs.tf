output "acr_login_server" {
  description = "La URL del Azure Container Registry (para empujar imágenes)"
  value       = azurerm_container_registry.acr.login_server
}

output "acr_admin_username" {
  description = "Usuario admin de ACR"
  value       = azurerm_container_registry.acr.admin_username
  sensitive   = true
}

output "acr_admin_password" {
  description = "Contraseña admin de ACR"
  value       = azurerm_container_registry.acr.admin_password
  sensitive   = true
}

output "api_url" {
  description = "URL pública de la API (FastAPI)"
  value       = "https://${azurerm_container_app.api.ingress[0].fqdn}"
}

output "dashboard_url" {
  description = "URL pública del Dashboard (Streamlit)"
  value       = "https://${azurerm_container_app.dashboard.ingress[0].fqdn}"
}
