variable "resource_group_name" {
  description = "El nombre del Resource Group en Azure"
  type        = string
  default     = "rg-anzencore-prod"
}

variable "location" {
  description = "La región de Azure donde se desplegarán los servicios"
  type        = string
  default     = "eastus2"
}

variable "acr_name" {
  description = "El nombre del Azure Container Registry (debe ser globalmente único y sin guiones)"
  type        = string
  default     = "acrAnzenCoreProd123"
}

variable "supabase_url" {
  description = "URL de Supabase"
  type        = string
}

variable "supabase_key" {
  description = "Anon/Service Key de Supabase"
  type        = string
  sensitive   = true
}

variable "image_tag" {
  description = "Tag de la imagen Docker a desplegar (proveido por GitHub Actions)"
  type        = string
  default     = "latest"
}
