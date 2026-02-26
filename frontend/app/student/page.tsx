const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "https://burhan-7.onrender.com";

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
