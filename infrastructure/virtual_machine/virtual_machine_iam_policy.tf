data "google_iam_policy" "finance_vm_iam_policy" {
  binding {
    role = "roles/iam.serviceAccountUser"
  }

  members = [
    "user:cloud@ineuron.ai"
  ]
}

resource "google_service_account_iam_policy" "finance_service_account_iam" {
  service_account_id = google_service_account.finance_service_account.name
  policy_data = data.google_iam_policy.finance_vm_iam_policy.policy_data
}
