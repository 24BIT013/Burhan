import { getBackendUrl } from "../lib/backend-url";
import OpenBackendLink from "../components/open-backend-link";

const backendUrl = getBackendUrl(process.env.NEXT_PUBLIC_BACKEND_URL);

export default function AdminPage() {
  return (
    <section className="card">
      <h2>Admin Access</h2>
      <p>Admin portal and Django admin are hosted on the backend service.</p>
      <div className="actions">
        <OpenBackendLink href={`${backendUrl}/admin-portal/login/`} label="Admin Portal Login" />
        <OpenBackendLink href={`${backendUrl}/django-admin/`} label="Django Admin" />
      </div>
    </section>
  );
}
