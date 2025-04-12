<template>
    <div class="login-container">
        <div class="login-form card">
            <div class="card-body">
                <h2 class="login-form-title">Login Skin Care</h2>
                <form @submit.prevent="onFinish">
                    <div class="form-group mb-3">
                        <input
                            type="text"
                            id="username"
                            v-model="username"
                            class="form-control"
                            required
                            placeholder="Username"
                        />
                    </div>
                    <div class="form-group mb-3">
                        <input
                            type="password"
                            id="password"
                            v-model="password"
                            class="form-control"
                            required
                            placeholder="Password"
                        />
                    </div>
                    <!-- <div class="form-check mb-3 d-flex remember_item"> -->
                    <!-- <input
                            type="checkbox"
                            id="remember"
                            v-model="remember"
                            class="form-check-input"
                        /> -->
                    <!-- <label
                            for="remember"
                            class="form-check-label text-white remember_label"
                        >
                            Remember username
                        </label> -->
                    <!-- </div> -->
                    <button
                        type="submit"
                        class="btn btn-primary w-100 login_btn"
                        :disabled="loading"
                    >
                        Log in
                    </button>

                    <NuxtLink class="createAccount" to="/registry"
                        >Create account</NuxtLink
                    >
                </form>
            </div>
            <div class="text-center mt-3">
                <p style="color: #fff; font-size: 11px">
                    Phần mềm quản lý quán bi-a
                    <i class="fa-solid fa-copyright"></i> SkinCare 2024 NuxtJs
                    by LuuDucQuang
                </p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { login } from "~/services/login.service";
import Cookies from "js-cookie";

definePageMeta({
    layout: "onlychildren",
});

const username = ref("");
const password = ref("");
const remember = ref(false);
const loading = ref(false);
const router = useRouter();

const onFinish = async () => {
    loading.value = true;
    try {
        const res = await login({
            username: username.value,
            password: password.value,
        });
        res.isRemember = remember.value;

        await loginSuccess(res);
    } catch (error) {
        console.error("Error logging in:", error);
    } finally {
        loading.value = false;
    }
};

const loginSuccess = async (res) => {
    Cookies.set("customer", JSON.stringify(res), { expires: 1 });
    router.push("/");
};
</script>

<style scoped>
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: darkcyan;
}

.login-form {
    width: 400px;
    padding: 20px;
    border-radius: 30px;
    background-color: #18a38d;
}

.login-form-title {
    text-align: center;
    font-size: 20px;
    margin-bottom: 20px;
    color: #fff;
}

.btn-primary {
    background-color: #20b2aa;
}

::placeholder {
    color: #c1c1c1;
    font-size: 14px;
}

input {
    font-size: 14px;
}

.remember_label {
    font-size: 14px;
}

.remember_label a {
    color: #ffffff;
}

.remember_label a:hover {
    color: #94ef91;
}

/* .remember_item {
    gap: 7px;
} */

.createAccount {
    color: #fff;
    padding-top: 5px;
    float: right;
    padding-top: 5px;
}

.createAccount:hover {
    color: #94ef91;
}

.remember_item input:hover {
    cursor: pointer;
}

.login_btn {
    border: 1px;
    transition: all 0.2s ease-in-out;
}

.login_btn:hover {
    transform: scale(1.05);
}
</style>
