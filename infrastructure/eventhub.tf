resource "azurerm_eventhub_namespace" "aks-keda-eh-lab" {
  name                = "aks-keda-eh-lab-${random_string.random-string.result}"
  resource_group_name = azurerm_resource_group.rg.name 
  location            = azurerm_resource_group.rg.location
  sku                 = "Standard"
  capacity            = 1
}

resource "azurerm_eventhub" "orders" {
  name           = "orders"
  namespace_id   = azurerm_eventhub_namespace.aks-keda-eh-lab.id
  partition_count = 2
  message_retention = 1
}

resource "azurerm_eventhub_consumer_group" "orders-consumer" {
  name                = "orders-consumer"
  namespace_name      = azurerm_eventhub_namespace.aks-keda-eh-lab.name
  eventhub_name       = azurerm_eventhub.orders.name
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_role_assignment" "aks-keda-eh-lab-app-data-owner" {
  scope                = azurerm_eventhub_namespace.aks-keda-eh-lab.id
  role_definition_name = "Azure Event Hubs Data Owner"
  principal_id         = azurerm_user_assigned_identity.aks-keda-eh-lab-app-identity.principal_id
}

resource "kubernetes_config_map" "event-hub-config" {
  metadata {
    name      = "event-hub-config"
    namespace = kubernetes_namespace.order.metadata.0.name
  }

  data = {
    EVENT_HUB_NAME     = "orders"
    EVENT_HUB_NAMESPACE = azurerm_eventhub_namespace.aks-keda-eh-lab.name
    HOST_NAME          = "${azurerm_eventhub_namespace.aks-keda-eh-lab.name}.servicebus.windows.net"
    CONSUMER_GROUP     = "orders-consumer"
  }

}