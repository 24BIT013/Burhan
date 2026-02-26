import { getBackendUrl } from "./lib/backend-url";
import OpenBackendLink from "./components/open-backend-link";

const backendUrl = getBackendUrl(process.env.NEXT_PUBLIC_BACKEND_URL);

export default function HomePage() {
  return (
    <section className="grid">
      <article className="card">
        <h2>Student Portal</h2>
        <p>Course registration, dashboard, and released results.</p>
        <OpenBackendLink href={`${backendUrl}/`} label="Open Student Login" />
      </article>
      <article className="card">
        <h2>Admin Portal</h2>
        <p>Admin registration, approvals, courses, and results.</p>
        <OpenBackendLink href={`${backendUrl}/admin-portal/login/`} label="Open Admin Portal" />
      </article>
      <article className="card">
        <h2>Django Admin</h2>
        <p>Built-in Django admin for superusers.</p>
        <OpenBackendLink href={`${backendUrl}/django-admin/`} label="Open Django Admin" />
      </article>
    </section>
  );
}
