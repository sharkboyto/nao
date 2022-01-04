# Nao - NVDA Gelişmiş OCR

* Yazarlar: Alessandro Albano, Davide De Carne, Simone Dal Maso
* [Kararlı sürümü][1] indir
* NVDA uyumluluğu: 2019.3 ve üstü

Nao (NVDA Advanced OCR), Windows'un modern sürümlerinde NVDA tarafından sağlanan standart OCR özelliklerini geliştiren bir eklentidir.
NVDA standart komutu, ekranı tanımak için Windows OCR'yi kullanırken, NAO, sabit sürücünüzde veya USB aygıtlarınızda kayıtlı dosyalar üzerinde OCR yapabilir.
Her türlü görüntüyü ve pdf'yi tanımak için NVDA-Shift-R'yi kullanın!
Odağı / imleci istediğiniz dosyanın üzerine getirin, açmayın, NVDA-Shift-r'ye basın.
Belge tanınacak ve tüm içeriği okumanıza izin veren basit bir metin düzenleme alanı açılacaktır.
Nao aynı zamanda çok sayfalı pdf'yi de işleyebilir, bu nedenle erişilebilir olmayan bir belgeniz varsa endişelenmeyin, Windows OCR tüm işi yapabilir.

## sistem gereksinimleri
Eklenti, yerleşik OCR özelliklerine sahip oldukları için Windows 10 ve Windows 11 sistemlerinde çalışır.
Nao, NVDA 2019.3 sürümünden itibaren sonrakilerle uyumludur, bu nedenle ekran okuyucunun eski sürümlerini kullanmayın.
Nao'nun Windows Gezgini, masaüstü veya Total Commander dosya yöneticisi ile çalıştığını unutmayın; 7zip veya Winrar gibi başka yazılımlar desteklenmediği için kullanmayın.

## Özellikler ve komutlar
* NVDA + Shift + R: dosya sisteminden her türlü görüntüyü ve pdf'yi tanı;
  * Önceki/sonraki sayfa: imleci çok sayfalı bir belgenin gerçek sayfaları arasında hareket ettir;
  * p: çok sayfalı bir belgede imleç konumuna göre sayfa numarasını oku.
  * l: çok sayfalı bir belgede imleç konumuna göre satır numarasını oku.
  * c: tüm belgeyi panoya kopyala.
  * s: Belgenin bir kopyasını metin biçiminde kaydet.
  * f: Metni ara ve dizeden önce ve sonra bulunan bazı kelimeleri oku.
* NVDA + Shift + Ctrl + R: tam ekran görüntüsü alır ve tanır.
  * Pencerede gezinmek ve odağı bir öğeye getirmek için standart NVDA komutlarının kullanılabileceğini unutmayın. Örneğin, yön tuşlarıyla hareket edebilir ve etkinleştirmek için bir düğme üzerinde enter tuşuna basabilirsiniz. Ayrıca NVDA + sayısal tuş takımı kombinasyonuna basarak ve ardından sol / sağ tıklayarak fareyi o konuma getirebilirsiniz.

Nao'nun kısayollarını yalnızca NVDA Girdi hareketleri iletişim kutusundan özelleştirebileceğinizi unutmayın. NVDA menüsünü açın, tercihlere gidin ve bu alt menüden girdi hareketlerini seçin.

Ayrıca ilerleme çubuğu penceresinden sadece "İptal"e basarak çok uzun bir Ocr işlemini kesmek de mümkündür; bu pencere ayrıca, kullanıcıyı her 5 saniyede bir güncelleyerek OCR durumu hakkında bilgi sağlar. Standart NVDA+u komutu ile ilerleme çubuğunda bilgi mesajlarını nasıl almak istediğinizi yapılandırabilirsiniz.

## Destek ve bağışlar
Nao tamamen ücretsizdir. Yine de, bu eklentinin geliştiricilerin boş zamanlarında yapıldığını unutmayın.
Bize yapabileceğiniz her türlü katkıyı takdir ediyoruz!
Çalışmamızın işe yarar  olduğunu ve hayatınızı iyileştirdiğini düşünüyorsanız, <a href="https://nvda-nao.org/donate">Bağış yapmayı değerlendirebilirsiniz.</a>
Bir hatayı bildirmek, yeni özellikler önermek, eklentiyi kendi dilinize çevirmek mi istiyorsunuz? Sizin için e-postamız var! support@nvda-nao.org adresine yazın, size yardımcı olmaktan memnuniyet duyarız.

## kronoloji
### 2021.2
* PDF ve görüntülerin OCR sonucu, basit işlemler için bazı kısayol tuşlarıyla birlikte yeni bir metin penceresinde sunulur.
* Xplorer dosya yöneticisi desteği.
* Nao kısayolları, NVDA Girdi Hareketleri iletişim kutusundan özelleştirilebilir.
* Nao yalnızca mümkün olduğunda çalışır, bu nedenle desteklenmeyen bir penceredeyseniz kısayol tuşu eklenti tarafından ele alınmaz; bu, daha önce kısayol tuşu Nao tarafından yanlış pencerelerde de   kullanıldığı için Excel ve Word kullanıcılarının NVDA-Shift-r tuşuna basamadıkları önemli bir sorunu düzeltti.
* Uzun bir OCR işlemi, ilerleme çubuğu penceresindeki "İptal" düğmesine basılarak durdurulabilir.
* Türkçe, Rusça, İspanyolca, Çince ve Fransızca çeviriler eklendi.
* Kullanıcılar projeye bağış yapabilirler.
* OCR'nin düzgün çalışmasını engelleyen dosya uzantılarında bazı karakterlerle ilgili bir hata düzeltildi.
### 2021.1
* İlk genel sürüm!


[1]: https://nvda-nao.org/download
