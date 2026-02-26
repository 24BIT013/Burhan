import { getBackendUrl } from "./lib/backend-url";

const backendUrl = getBackendUrl(process.env.NEXT_PUBLIC_BACKEND_URL);

export default function HomePage() {
  return (
    <section className="grid">
      <article className="card">
        <h2>Student Portal</h2>
        <p>Course registration, dashboard, and released results.</p>
        <a href={`${backendUrl}/`} target="_blank" rel="noreferrer">
          Open Student Login
        </a>
      </article>
      <article className="card">
        <h2>Admin Portal</h2>
        <p>Admin registration, approvals, courses, and results.</p>
        <a href={`${backendUrl}/admin-portal/login/`} target="_blank" rel="noreferrer">
          Open Admin Portal
        </a>
      </article>
      <article className="card">
        <h2>Django Admin</h2>
        <p>Built-in Django admin for superusers.</p>
        <a href={`${backendUrl}/django-admin/`} target="_blank" rel="noreferrer">
          Open Django Admin
        </a>
      </article>
    </section>
  );
}
