terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.13.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

resource "azurerm_resource_group" "pdfextract" {
  name     = "pdfextract"
  location = "UK South"

  tags = {
    source  = "terraform",
    app     = "worthit",
    service = "pdfextract"
  }
}

resource "azurerm_storage_account" "pdfextract" {
  name                     = "pdfextract202501041224"
  resource_group_name      = azurerm_resource_group.pdfextract.name
  location                 = azurerm_resource_group.pdfextract.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"

  tags = {
    source  = "terraform",
    app     = "worthit",
    service = "pdfextract"
  }
}

resource "azurerm_storage_container" "pdfextract_user_uploads" {
  name                  = "pdfextract-user-uploads"
  storage_account_id    = azurerm_storage_account.pdfextract.id
  container_access_type = "private"
}

# Define a lifecycle management policy
resource "azurerm_storage_management_policy" "pdfextract_storage_policy" {
  storage_account_id = azurerm_storage_account.pdfextract.id

  rule {
    name    = "pdfextract-user-uploads-deletion"
    enabled = true

    filters {
      blob_types = ["blockBlob"]
    }

    actions {
      base_blob {
        delete_after_days_since_creation_greater_than = 1
      }
      snapshot {
        delete_after_days_since_creation_greater_than = 1
      }
      version {
        delete_after_days_since_creation = 1
      }
    }
  }
}

# App Service Plan
resource "azurerm_service_plan" "pdfextract" {
  name                = "pdfextract"
  location            = azurerm_resource_group.pdfextract.location
  resource_group_name = azurerm_resource_group.pdfextract.name
  os_type             = "Linux"
  sku_name            = "Y1"
  #   kind                = "FunctionApp" # Indicates it's for a Function App

  tags = {
    source  = "terraform",
    app     = "worthit",
    service = "pdfextract"
  }
}

resource "azurerm_linux_function_app" "pdfextract" {
  name                = "pdfextract-app"
  resource_group_name = azurerm_resource_group.pdfextract.name
  location            = azurerm_resource_group.pdfextract.location

  storage_account_name       = azurerm_storage_account.pdfextract.name
  storage_account_access_key = azurerm_storage_account.pdfextract.primary_access_key
  service_plan_id            = azurerm_service_plan.pdfextract.id

  # https_only = true
  app_settings = {
    functions_extension_version = "~4"
    FUNCTIONS_WORKER_RUNTIME    = "PYTHON"
    WEBSITE_RUN_FROM_PACKAGE    = "1"
  }

  site_config {
    application_stack {
      python_version = 3.11
    }

  }

  tags = {
    source  = "terraform",
    app     = "worthit",
    service = "pdfextract"
  }
}
