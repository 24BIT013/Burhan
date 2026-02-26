import { getBackendUrl } from "../lib/backend-url";

const backendUrl = getBackendUrl(process.env.NEXT_PUBLIC_BACKEND_URL);

export default function StudentPage() {
  return (
    <section className="card">
      <h2>Student Access</h2>
      <p>Use your student credentials from the backend system.</p>
      <a href={`${backendUrl}/`} target="_blank" rel="noreferrer">
        Continue to Student Login
      </a>
    </section>
  );
}
