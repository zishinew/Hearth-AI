export default function Footer() {
  return (
    <footer className="bg-[#FAFAF9] border-t border-slate-200 py-8 px-4">
      <div className="mx-auto max-w-6xl">
        <div className="flex flex-col items-center justify-center gap-4 text-center sm:flex-row sm:justify-between">
          <p className="text-base text-slate-600">
            © {new Date().getFullYear()} ForeverHome. All rights reserved.
          </p>
          <div className="flex gap-6">
            <a
              href="#"
              className="text-base text-slate-600 hover:text-slate-900 transition-colors"
            >
              Privacy Policy
            </a>
            <a
              href="#"
              className="text-base text-slate-600 hover:text-slate-900 transition-colors"
            >
              Terms of Service
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
