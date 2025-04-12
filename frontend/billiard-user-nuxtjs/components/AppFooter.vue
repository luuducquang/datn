<template>
    <footer class="bg-light pt-4">
        <div class="container-fluid support_content">
            <div class="container">
                <div class="row support">
                    <div class="col-md-3 col-sm-6">
                        <h5 class="title-footer">HỖ TRỢ KHÁCH HÀNG</h5>
                        <ul class="list-unstyled">
                            <li>
                                <a href="#"
                                    ><i class="fa fa-play"></i> Hướng dẫn mua
                                    hàng</a
                                >
                            </li>
                            <li>
                                <a href="#"
                                    ><i class="fa fa-play"></i> Chính sách vận
                                    chuyển</a
                                >
                            </li>
                            <li>
                                <a href="#"
                                    ><i class="fa fa-play"></i> Chính sách bảo
                                    hành</a
                                >
                            </li>
                            <li>
                                <a href="#"
                                    ><i class="fa fa-play"></i> Chính sách bảo
                                    mật thông tin</a
                                >
                            </li>
                            <li>
                                <a href="#"
                                    ><i class="fa fa-play"></i> Chính sách đổi
                                    trả</a
                                >
                            </li>
                        </ul>
                    </div>
                    <div class="col-md-3 col-sm-6">
                        <h5 class="title-footer">VỀ CHÚNG TÔI</h5>
                        <ul class="list-unstyled">
                            <li>
                                <a href="#"
                                    ><i class="fa fa-play"></i> Sứ mệnh và tầm
                                    nhìn</a
                                >
                            </li>
                            <li>
                                <a href="#"
                                    ><i class="fa fa-play"></i> Giới thiệu công
                                    ty</a
                                >
                            </li>
                            <li>
                                <a href="#"><i class="fa fa-play"></i> Blog</a>
                            </li>
                            <li>
                                <a href="#"
                                    ><i class="fa fa-play"></i> Liên hệ</a
                                >
                            </li>
                        </ul>
                    </div>
                    <div class="col-md-3 col-sm-6">
                        <h5 class="title-footer">MẠNG XÃ HỘI</h5>
                        <div>
                            <a href="https://www.facebook.com"
                                ><i class="fab fa-facebook-square fa-2x"></i
                            ></a>
                            <a href="https://www.instagram.com/kuanq_ne/"
                                ><i class="fab fa-instagram fa-2x"></i
                            ></a>
                        </div>
                    </div>
                    <div class="col-md-3 col-sm-6">
                        <h5 class="title-footer">FANPAGE</h5>
                        <a target="_blank" href="https://www.facebook.com">
                            <img src="" alt="Fanpage" class="img-fluid" />
                        </a>
                    </div>
                </div>
            </div>
        </div>
        <div class="container-fluid nocopy_content">
            <div class="container">
                <div class="row nocopy">
                    <div class="col text-center">
                        <p class="copyright">Copyright © Q-Billiard Club</p>
                    </div>
                </div>
            </div>
        </div>
    </footer>
</template>

<script setup lang="ts"></script>

<style scoped>
.footer {
    background-color: #f8f9fa;
}

.title-footer {
    font-weight: bold;
    margin-bottom: 15px;
}

.list-unstyled a {
    text-decoration: none;
    color: #fff;
    display: block;
    margin-bottom: 10px;
}

a {
    color: #fff;
}

a:hover,
i:hover {
    color: var(--color-primary-two) !important;
}

.list-unstyled a:hover {
    color: #007bff;
}

.fa-2x {
    margin-right: 10px;
}

.img-fluid {
    max-width: 100%;
    height: auto;
}

.copyright {
    font-size: 14px;
    color: #6c757d;
}

.support_content {
    background-color: #63666b;
}

.support {
    background-color: #63666b;
    padding: 20px 0;
}
.nocopy_content {
    background-color: #444444;
}
.nocopy {
    padding-top: 15px;
    background-color: #444444;
}

.copyright {
    color: #fff;
}

h5 {
    color: #fff;
}
</style>
