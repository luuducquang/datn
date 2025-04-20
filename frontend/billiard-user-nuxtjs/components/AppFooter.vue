<template>
    <footer class="footer">
      <div class="container py-5">
        <div class="row">
          <div class="col-md-3 col-sm-6 mb-4">
            <h5 class="footer-title">HỖ TRỢ</h5>
            <ul class="footer-list">
              <li><a href="#">Hướng dẫn mua hàng</a></li>
              <li><a href="#">Chính sách vận chuyển</a></li>
              <li><a href="#">Chính sách bảo hành</a></li>
              <li><a href="#">Chính sách bảo mật</a></li>
              <li><a href="#">Chính sách đổi trả</a></li>
            </ul>
          </div>
          <div class="col-md-3 col-sm-6 mb-4">
            <h5 class="footer-title">VỀ CHÚNG TÔI</h5>
            <ul class="footer-list">
              <li><a href="#">Sứ mệnh & tầm nhìn</a></li>
              <li><a href="#">Giới thiệu công ty</a></li>
              <li><a href="#">Blog</a></li>
              <li><a href="#">Liên hệ</a></li>
            </ul>
          </div>
          <div class="col-md-3 col-sm-6 mb-4">
            <h5 class="footer-title">KẾT NỐI</h5>
            <div class="social-icons">
              <a href="https://www.facebook.com" target="_blank"><i class="fab fa-facebook-f"></i></a>
              <a href="https://www.instagram.com" target="_blank"><i class="fab fa-instagram"></i></a>
              <a href="https://www.youtube.com" target="_blank"><i class="fab fa-youtube"></i></a>
            </div>
          </div>
          <div class="col-md-3 col-sm-6 mb-4">
            <h5 class="footer-title">FANPAGE</h5>
            <a href="https://www.facebook.com" target="_blank">
              <img src="http://127.0.0.1:8000/static/uploads/banner-thế-giới-bida.jpg" alt="Fanpage" class="img-fluid rounded shadow" />
            </a>
          </div>
        </div>
      </div>
      <div class="footer-bottom text-center py-3">
        <p>© 2025 Q-Billiard Club. All rights reserved.</p>
      </div>
    </footer>
  </template>
  
  <style scoped>
  .footer {
    background-color: #1d1e22;
    color: #fff;
  }
  
  .footer-title {
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 15px;
    color: var(--color-primary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  
  .footer-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .footer-list li {
    margin-bottom: 10px;
  }
  
  .footer-list a {
    color: #ccc;
    text-decoration: none;
    font-size: 14px;
    transition: color 0.2s ease;
  }
  
  .footer-list a:hover {
    color: var(--color-primary);
  }
  
  .social-icons a {
    display: inline-block;
    margin-right: 15px;
    font-size: 20px;
    color: #ccc;
    transition: color 0.3s;
  }
  
  .social-icons a:hover {
    color: var(--color-primary);
  }
  
  .footer-bottom {
    background-color: #151618;
    color: #aaa;
    font-size: 13px;
  }
  </style>
  