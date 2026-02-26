const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "https://burhan-7.onrender.com";

export default function AdminPage() {
  return (
    <section className="card">
      <h2>Admin Access</h2>
      <p>Admin portal and Django admin are hosted on the backend service.</p>
      <div className="actions">
        <a href={`${backendUrl}/admin-portal/login/`} target="_blank" rel="noreferrer">
          Admin Portal Login
        </a>
        <a href={`${backendUrl}/django-admin/`} target="_blank" rel="noreferrer">
          Django Admin
        </a>
      </div>
    </section>
  );
}
