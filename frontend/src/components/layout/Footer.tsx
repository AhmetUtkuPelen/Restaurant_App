'use client';

import React from 'react';
import Link from 'next/link';
import { Github, Mail, Linkedin, Braces } from 'lucide-react';

export default function Footer() {
  const CurrentYear : number = 2025;
  return (
    <footer className="footer footer-center p-10 bg-base-200 text-base-content rounded">
      <nav className="grid grid-flow-col gap-4">
        <Link href="/about" className="link link-hover">About</Link>
        <Link href="/contact" className="link link-hover">Contact</Link>
        <Link href="/privacy" className="link link-hover">Privacy</Link>
        <Link href="/terms" className="link link-hover">Terms</Link>
      </nav>
      
      <nav>
        <div className="grid grid-flow-col gap-4">
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-ghost btn-circle"
            aria-label="GitHub"
          >
            <Github size={26} className='text-blue-600' />
          </a>
          <a
            href="https://twitter.com"
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-ghost btn-circle"
            aria-label="Twitter"
          >
            <Mail size={26} className='text-blue-600' />
          </a>
          <a
            href="https://linkedin.com"
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-ghost btn-circle"
            aria-label="LinkedIn"
          >
            <Linkedin size={26} className='text-blue-600' />
          </a>
        </div>
      </nav>
      
      <aside className="flex items-center gap-2">
        <p className="flex items-center gap-1">
          Made with using <Braces size={18} className="text-red-500" />
        </p>
        <div className="flex items-center gap-2">
          <div className="badge badge-primary">Next.js</div>
          <div className="badge badge-success">FastAPI</div>
          <div className="badge badge-accent">Socket.IO</div>
          <div className="badge badge-neutral">DaisyUI</div>
        </div>
      </aside>
      
      <aside>
        <p>Copyright © {CurrentYear} - Real-time Chat Application</p>
      </aside>
    </footer>
  );
}
