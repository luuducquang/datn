<template>
    <el-card title="Login Admin" class="login-card">
        <el-form
            :model="formState"
            @submit.prevent="handleSubmit"
            label-position="top"
            autocomplete="on"
        >
            <el-form-item
                label="Tài khoản"
                :error="email.errorMsg"
                :status="email.validateStatus"
            >
                <el-input
                    v-model="formState.email"
                    placeholder="Vui lòng nhập tài khoản"
                    name="email"
                    type="email"
                    autocomplete="username"
                />
            </el-form-item>

            <el-form-item
                label="Mật khẩu"
                :error="password.errorMsg"
                :status="password.validateStatus"
            >
                <el-input
                    v-model="formState.password"
                    placeholder="Vui lòng nhập mật khẩu"
                    name="password"
                    type="password"
                    autocomplete="current-password"
                />
            </el-form-item>

            <el-form-item>
                <el-button
                    type="primary"
                    native-type="submit"
                    :loading="loading"
                    block
                    >Login</el-button
                >
            </el-form-item>
        </el-form>
    </el-card>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { login } from "~/services/login.service";
import { useUserStore } from "~/store";

const Notification = (
    message: string,
    type: "success" | "warning" | "error"
) => {
    ElMessage({
        message: message,
        type: type,
    });
};

const formState = reactive({
    email: "",
    password: "",
});

const email = ref({
    validateStatus: "",
    errorMsg: "",
});

const password = ref({
    validateStatus: "",
    errorMsg: "",
});

const loading = ref(false);
const userStore = useUserStore();
const router = useRouter();

const validateForm = () => {
    let isValid = true;
    if (!formState.email) {
        email.value.validateStatus = "error";
        email.value.errorMsg = "Vui lòng nhập tài khoản";
        isValid = false;
    } else {
        email.value.validateStatus = "";
        email.value.errorMsg = "";
    }

    if (!formState.password) {
        password.value.validateStatus = "error";
        password.value.errorMsg = "Vui lòng nhập mật khẩu";
        isValid = false;
    } else {
        password.value.validateStatus = "";
        password.value.errorMsg = "";
    }

    return isValid;
};

const handleSubmit = async () => {
    if (validateForm()) {
        loading.value = true;
        try {
            setTimeout(async function () {
                try {
                    const res = await login({
                        email: formState.email,
                        password: formState.password,
                    });
                    console.log(res);
                    if (
                        res?.role_name === "ADMIN" ||
                        res?.role_name === "EMPLOYEE"
                    ) {
                        loading.value = false;
                        userStore.setUser(res);
                        router.push("/").then(() => {
                            window.location.reload();
                        });

                        Notification(
                            `Đăng nhập thành công. Xin chào, ${res?.fullname}`,
                            "success"
                        );
                    } else {
                        Notification(
                            "Tài khoản khách hàng không thể vào đây!",
                            "warning"
                        );
                        loading.value = false;
                    }
                } catch (error) {
                    Notification(
                        "Tài khoản hoặc mật khẩu không chính xác!",
                        "warning"
                    );
                    loading.value = false;
                }
            }, 1000);
        } catch (error) {
            console.error("Error submitting form:", error);
        }
    }
};
</script>

<style scoped>
.login-card {
    max-width: 400px;
    margin: 100px auto;
    padding: 20px;
}
</style>
