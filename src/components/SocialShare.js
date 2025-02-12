import React from 'react';
import {
    FacebookShareButton,
    TwitterShareButton,
    WhatsappShareButton,
    LinkedinShareButton,
    TelegramShareButton,
    FacebookIcon,
    TwitterIcon,
    WhatsappIcon,
    LinkedinIcon,
    TelegramIcon
} from 'react-share';
import { useTranslation } from 'react-i18next';
import './SocialShare.css';

const SocialShare = ({ vehicleData, predictionData }) => {
    const { t } = useTranslation();
    
    // Paylaşım URL'i (kendi domain'inize göre güncelleyin)
    const shareUrl = 'https://ekspertiz.com/rapor';
    
    // Paylaşım metni oluştur
    const getShareTitle = () => {
        const title = t('share.title', {
            brand: vehicleData.marka,
            model: vehicleData.model,
            year: vehicleData.yil
        });
        
        const details = t('share.details', {
            price: predictionData.deger,
            confidence: predictionData.guvenOrani
        });
        
        return `${title}\n${details}`;
    };

    return (
        <div className="social-share">
            <h4>{t('share.shareReport')}</h4>
            <div className="share-buttons">
                <FacebookShareButton
                    url={shareUrl}
                    quote={getShareTitle()}
                    className="share-button"
                >
                    <FacebookIcon size={32} round />
                </FacebookShareButton>

                <TwitterShareButton
                    url={shareUrl}
                    title={getShareTitle()}
                    className="share-button"
                >
                    <TwitterIcon size={32} round />
                </TwitterShareButton>

                <WhatsappShareButton
                    url={shareUrl}
                    title={getShareTitle()}
                    className="share-button"
                >
                    <WhatsappIcon size={32} round />
                </WhatsappShareButton>

                <LinkedinShareButton
                    url={shareUrl}
                    title={t('share.linkedinTitle')}
                    summary={getShareTitle()}
                    className="share-button"
                >
                    <LinkedinIcon size={32} round />
                </LinkedinShareButton>

                <TelegramShareButton
                    url={shareUrl}
                    title={getShareTitle()}
                    className="share-button"
                >
                    <TelegramIcon size={32} round />
                </TelegramShareButton>
            </div>
        </div>
    );
};

export default SocialShare;