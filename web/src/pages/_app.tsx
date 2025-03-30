import "@/styles/global.css";
import type { AppProps } from "next/app";
import Head from "next/head";




export default function App({ Component, pageProps }: AppProps) {
  return(
    <>
<Head>
  <link rel="icon" href="/SkyGuardian-logo-drone.png" />
  <title>SkyGuardian</title>
</Head>
  <Component {...pageProps} />
  </>);
}
