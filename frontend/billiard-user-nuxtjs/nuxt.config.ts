// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: "2024-04-03",
    devtools: { enabled: false },
    ssr: true,
    typescript: {
        strict: true,
    },
    modules: ["@pinia/nuxt"],

    css: ["~/assets/style.css"],

    app: {
        head: {
            charset: "utf-8",
            viewport: "width=device-width, initial-scale=1",
            link: [
                {
                    href: "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css",
                    rel: "stylesheet",
                    integrity:
                        "sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC",
                    crossorigin: "anonymous",
                },
                {
                    rel: "preconnect",
                    href: "https://fonts.googleapis.com",
                },
                {
                    rel: "preconnect",
                    href: "https://fonts.gstatic.com",
                },
                {
                    href: "https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap",
                    rel: "stylesheet",
                },
                {
                    href: "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css",
                    rel: "stylesheet",
                },
            ],
            script: [
                {
                    src: "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js",
                    integrity:
                        "sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM",
                    crossorigin: "anonymous",
                },
            ],
        },
    },
});
