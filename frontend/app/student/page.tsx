import { getBackendUrl } from "../lib/backend-url";
import OpenBackendLink from "../components/open-backend-link";

const backendUrl = getBackendUrl(process.env.NEXT_PUBLIC_BACKEND_URL);

export default function StudentPage() {
  return (
    <section className="card">
      <h2>Student Access</h2>
      <p>Use your student credentials from the backend system.</p>
      <OpenBackendLink href={`${backendUrl}/`} label="Continue to Student Login" />
    </section>
  );
}
